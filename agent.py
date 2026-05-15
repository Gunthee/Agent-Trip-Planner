import json
import os
import re
from typing import Callable, Dict, Any

from logger_utils import console, log_step, log_thought, log_action, log_observation, log_final_answer
from prompts import build_prompt

MAX_ITERATIONS = 10

# ---------------------------------------------------------------------------
# LLM backend helpers
# ---------------------------------------------------------------------------

def _call_ollama(model: str, prompt: str) -> str:
    import ollama
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1, "num_predict": 1024},
    )
    return response["message"]["content"]


def _call_groq(model: str, prompt: str) -> str:
    import requests
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable not set.")
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1024,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class TravelAgent:
    def __init__(self, model_name: str = "qwen2.5:7b", backend: str = "ollama"):
        self.model_name = model_name
        self.backend = backend  # "ollama" or "groq"
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func

    def _call_llm(self, prompt: str) -> str:
        if self.backend == "groq":
            return _call_groq(self.model_name, prompt)
        return _call_ollama(self.model_name, prompt)

    def _parse(self, text: str) -> Dict[str, Any]:
        result = {"thought": None, "action": None, "action_input": None, "final_answer": None}

        thought_m = re.search(r"Thought:\s*(.+?)(?=Action:|Final Answer:|$)", text, re.DOTALL | re.IGNORECASE)
        if thought_m:
            result["thought"] = thought_m.group(1).strip()

        final_m = re.search(r"Final Answer:\s*(.+?)$", text, re.DOTALL | re.IGNORECASE)
        if final_m:
            result["final_answer"] = final_m.group(1).strip()
            return result

        action_m = re.search(r"Action:\s*(\w+)", text, re.IGNORECASE)
        if action_m:
            result["action"] = action_m.group(1).strip()

        input_m = re.search(r"Action Input:\s*(\{.+?\})", text, re.DOTALL | re.IGNORECASE)
        if input_m:
            raw = re.sub(r"\s+", " ", input_m.group(1).strip())
            try:
                result["action_input"] = json.loads(raw)
            except json.JSONDecodeError:
                result["action_input"] = {}

        return result

    def run(self, user_query: str) -> str:
        console.rule("[bold blue]Travel Planning Agent[/bold blue]")
        log_step("Query", user_query, "bold white")
        log_step("Backend", f"{self.backend} / {self.model_name}", "dim")

        history = ""

        for iteration in range(1, MAX_ITERATIONS + 1):
            log_step("Iteration", f"{iteration}/{MAX_ITERATIONS}", "dim")

            prompt = build_prompt(user_query, history)

            try:
                llm_text = self._call_llm(prompt)
            except Exception as e:
                log_step("Error", f"LLM call failed: {e}", "red")
                return f"LLM error: {e}"

            parsed = self._parse(llm_text)

            if parsed["thought"]:
                log_thought(parsed["thought"])

            if parsed["final_answer"]:
                log_final_answer(parsed["final_answer"])
                return parsed["final_answer"]

            action = parsed.get("action")
            action_input = parsed.get("action_input") or {}

            if not action:
                log_step("Warning", "Could not parse an Action — stopping.", "red")
                return "Could not determine next action. Please rephrase your query."

            log_action(action, action_input)

            if action not in self.tools:
                observation = f"Unknown tool '{action}'. Available tools: {', '.join(self.tools)}"
            else:
                try:
                    observation = str(self.tools[action](**action_input))
                except TypeError as e:
                    observation = f"Tool '{action}' called with wrong arguments: {e}"
                except Exception as e:
                    observation = f"Tool '{action}' error: {e}"

            log_observation(observation)

            history += (
                f"Thought: {parsed['thought'] or ''}\n"
                f"Action: {action}\n"
                f"Action Input: {json.dumps(action_input)}\n"
                f"Observation: {observation}\n\n"
            )

        return "Reached maximum iterations without a final answer."
