from logger_utils import log_retrieved_docs

_vector_store = None


def init_search_tool(vector_store):
    global _vector_store
    _vector_store = vector_store


def semantic_search(query: str, n_results: int = 3) -> str:
    """Search the travel knowledge base using semantic similarity."""
    if _vector_store is None or _vector_store.count() == 0:
        return "Knowledge base is empty. Please add PDF or TXT files to the data/ folder and restart."

    docs, scores, metas = _vector_store.search(query, n_results=n_results)
    log_retrieved_docs(docs, scores, metas)

    if not docs:
        return "No relevant information found."

    parts = [f"Found {len(docs)} relevant passages:\n"]
    for i, (doc, score, meta) in enumerate(zip(docs, scores, metas), 1):
        src = meta.get("source", "unknown")
        parts.append(f"[{i}] relevance={score:.4f}  source={src}\n{doc}\n")
    return "\n".join(parts)
