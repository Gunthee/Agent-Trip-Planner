from typing import List, Tuple
import chromadb
from sentence_transformers import SentenceTransformer


class TravelVectorStore:
    COLLECTION = "travel_knowledge"

    def __init__(self, persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, documents: List[str], metadatas: List[dict] = None):
        if not documents:
            return
        embeddings = self.model.encode(documents, show_progress_bar=True).tolist()
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas or [{} for _ in documents],
        )
        print(f"Indexed {len(documents)} chunks into ChromaDB")

    def search(self, query: str, n_results: int = 3) -> Tuple[List[str], List[float], List[dict]]:
        emb = self.model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=emb, n_results=n_results)
        docs = results["documents"][0]
        scores = [1.0 - d for d in results["distances"][0]]  # cosine similarity
        metas = results["metadatas"][0]
        return docs, scores, metas

    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        self.client.delete_collection(self.COLLECTION)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
