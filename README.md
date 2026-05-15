# Travel Planning Agentic RAG

ระบบ AI Agent สำหรับวางแผนทริปต่างประเทศ โดยใช้ Retrieval-Augmented Generation (RAG)

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│           Travel Agent (ReAct Loop)      │
│                                          │
│  Thought → Action → Tool Call           │
│       ↑                  │               │
│       └──── Observation ─┘               │
└─────────────────────────────────────────┘
         │           │           │
         ▼           ▼           ▼
  semantic_search  get_exchange  search_hotels
  (ChromaDB RAG)   _rate (API)   (mock DB)
         │
         ▼
  all-MiniLM-L6-v2
  (Embedding Model)
         │
         ▼
    PDF / TXT files
    (data/ folder)
```

## Tech Stack

| Component        | Technology                          |
|-----------------|-------------------------------------|
| LLM             | Ollama — qwen2.5:7b (open-source ≤50B) |
| Embedding       | sentence-transformers all-MiniLM-L6-v2 |
| Vector DB       | ChromaDB (persistent)               |
| Agent Pattern   | Custom ReAct loop (no framework)    |
| Exchange Rate   | Frankfurter API (free, no key)      |
| Logging         | Rich (terminal color output)        |

## Tools

| Tool | Description |
|------|-------------|
| `semantic_search` | ค้นหาข้อมูลจาก knowledge base (PDF/TXT) ด้วย vector similarity |
| `get_exchange_rate` | ดึงอัตราแลกเปลี่ยนเงินแบบ real-time จาก frankfurter.app |
| `search_hotels` | ค้นหาโรงแรมพร้อม filter ราคา/rating |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and start Ollama
```bash
# Install Ollama from https://ollama.com
ollama pull qwen2.5:7b
```

### 3. Add travel documents
Put PDF or TXT files in the `data/` folder. A sample `travel_guide.txt` is already included.

### 4. Run
```bash
python main.py
```

To use a different Ollama model:
```bash
set OLLAMA_MODEL=llama3.2:3b
python main.py
```

### 5. Re-index documents
Delete the `chroma_db/` folder and restart to re-index from scratch:
```bash
rmdir /s /q chroma_db
python main.py
```

## Project Structure

```
agent_rag/
├── main.py              # Entry point
├── agent.py             # ReAct agent loop
├── prompts.py           # System prompts
├── logger_utils.py      # Rich terminal logging
├── rag/
│   ├── loader.py        # PDF + TXT document loader
│   └── vector_store.py  # ChromaDB wrapper + embedding
├── tools/
│   ├── semantic_search.py  # RAG search tool
│   ├── exchange_rate.py    # Currency API tool
│   └── hotel_search.py     # Hotel search tool
├── data/
│   └── travel_guide.txt    # Sample knowledge base
└── requirements.txt
```

## Observability

ทุก step ของ Agent จะแสดงใน terminal พร้อม timestamp และ color coding:
- **Yellow** — Agent Thought (reasoning)
- **Cyan** — Action (tool call + input)
- **Green** — Observation (tool result + retrieved docs with scores)
- **Magenta** — Final Answer

Retrieved documents แสดง relevance score (cosine similarity 0–1) และ source file.

## Example Queries

- `วางแผนทริป 5 วัน ไปญี่ปุ่น งบ 50,000 บาท`
- `แนะนำโรงแรมในโซล เกาหลี ราคาไม่เกิน $100 ต่อคืน`
- `ต้องเตรียมอะไรบ้างถ้าจะไปปารีส รวมถึงวีซ่าและค่าเงิน`
- `plan a 3-day trip to Singapore on a budget`
