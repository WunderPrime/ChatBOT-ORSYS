from langchain_chroma import Chroma
from embeddings_langchain import embeddings_model

vector_store = Chroma(
    collection_name="schema_tables",
    embedding_function=embeddings_model,
    persist_directory="./chroma_data_laungchain",
)

def index_schema(table_descriptions):
    vector_store.add_texts(texts=table_descriptions)

def retrieve_relevant_tables(question, top_k=3):
    results = vector_store.similarity_search(question, k=top_k)
    return [doc.page_content for doc in results]