# test_langchain_vector.py
from vector_store_langchain import index_schema, retrieve_relevant_tables
from schema import get_schema_list

index_schema(get_schema_list())
results = retrieve_relevant_tables("je veux voir les réclamations des clients", top_k=3)
print(results)