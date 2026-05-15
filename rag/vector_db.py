import chromadb
from chromadb.utils import embedding_functions
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas as pd 
from data_preprocessing import clean_text
import os

CHROMA_DATA_PATH = "vector_db/"
EMBED_MODEL = "paraphrase-multilingual-mpnet-base-v2"


def init_vector_db():
    print("Initializing ChromaDB vector database...")
    # Create client (Database)
    
    if not os.path.exists(CHROMA_DATA_PATH):
        client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    else:
        print(f"ChromaDB data path '{CHROMA_DATA_PATH}' already exists. Skipping client creation.")
        return

    # Create embedding function from sentence-transformer
    print("Creating embedding function...")
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    # Create collection (Table)
    print("Creating collection...")
    COLLECTION_NAME = "tours_collection"

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func, # embbeding function from sentence-transformer
        metadata={"hnsw:space": "cosine"}, # use cosine similarity to find closeness result. You can choose another include l2, ip.
    )   

    # Load data
    print("Loading data...")
    try:
        df = pd.read_csv('tours_merged_cleaned2.csv')
    except FileNotFoundError:
        print("File 'tours_merged_cleaned.csv' not found. Please check the file path.")
        return

    # Preprocess data
    print("Preprocessing data...")
    df['description'] = df['description'].apply(clean_text)

    # Prepare data to add to collection
    print("Preparing data...")
    ids = []
    documents = []
    metadatas = []

    for index, row in df.iterrows():
        ids.append(str(index))
        documents.append(str(row["description"]))
        metadatas.append({
        "program_tour": str(row["program_tour"]),
        "url": str(row["url"]),
        "price": str(row["price"]),
        "region": str(row["region"])
    })

    # Add data to collection
    print("Adding data to collection...")
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print("Data added to ChromaDB successfully.")
    print("Total records:", collection.count())
    return 

if __name__ == "__main__":
    init_vector_db()