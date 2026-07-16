import chromadb
from embeddings import get_embeddings

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="schema_tables")

def index_schema(table_desscription):
    for i, table_text in enumerate(table_desscription):
        embedding = get_embeddings(table_text)
        collection.upsert(
            ids=[f"table_{i}"],
            embeddings=[embedding],
            documents=[table_text],
        )


def retrieve_relevant_tables(question, top_k=3):
    question_embedding = get_embeddings(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )
    return results["documents"][0]