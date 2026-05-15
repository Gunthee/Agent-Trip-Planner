import os
from typing import List, Tuple

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


def _split_text(text: str, chunk_size: int = 400, overlap: int = 60) -> List[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def _load_pdf(file_path: str) -> List[str]:
    if not HAS_PYPDF:
        print("pypdf not installed, skipping PDF:", file_path)
        return []
    reader = pypdf.PdfReader(file_path)
    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            chunks.extend(_split_text(text))
    return chunks


def _load_txt(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return _split_text(f.read())


def load_documents_from_dir(data_dir: str) -> Tuple[List[str], List[dict]]:
    all_chunks, metadatas = [], []
    for fname in os.listdir(data_dir):
        fpath = os.path.join(data_dir, fname)
        if not os.path.isfile(fpath):
            continue
        if fname.lower().endswith(".pdf"):
            chunks = _load_pdf(fpath)
        elif fname.lower().endswith(".txt"):
            chunks = _load_txt(fpath)
        else:
            continue
        print(f"  Loaded {len(chunks)} chunks from {fname}")
        for c in chunks:
            all_chunks.append(c)
            metadatas.append({"source": fname})
    return all_chunks, metadatas
