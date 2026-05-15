import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()


def _ts():
    return datetime.datetime.now().strftime("%H:%M:%S")


def log_step(step_type: str, content: str, color: str = "cyan"):
    console.print(f"[dim]{_ts()}[/dim] [{color}][{step_type}][/{color}] {content}")


def log_thought(thought: str):
    console.print(Panel(thought.strip(), title="[yellow]Thought[/yellow]", border_style="yellow"))


def log_action(action: str, action_input: dict):
    body = f"Tool: [bold cyan]{action}[/bold cyan]\nInput: {action_input}"
    console.print(Panel(body, title="[cyan]Action[/cyan]", border_style="cyan"))


def log_observation(observation: str):
    preview = observation[:800] + "..." if len(observation) > 800 else observation
    console.print(Panel(preview, title="[green]Observation[/green]", border_style="green"))


def log_final_answer(answer: str):
    console.print(Panel(answer, title="[bold magenta]Final Answer[/bold magenta]", border_style="magenta"))


def log_retrieved_docs(docs: list, scores: list, metadatas: list = None):
    console.print("\n[bold blue]--- Retrieved Documents ---[/bold blue]")
    for i, (doc, score) in enumerate(zip(docs, scores), 1):
        source = metadatas[i - 1].get("source", "unknown") if metadatas else "unknown"
        console.print(f"  [dim][{i}][/dim] Score: [green]{score:.4f}[/green]  Source: [blue]{source}[/blue]")
        console.print(f"      {doc[:200].strip()}...")
    console.print()
