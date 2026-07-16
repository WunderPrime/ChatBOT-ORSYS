from vector_store import index_schema, retrieve_relevant_tables
from schema import get_schema_list

index_schema(get_schema_list())

results = retrieve_relevant_tables("Je veux voir les commandes passées par l'utilisateur avec l'ID 123", top_k=5)
print(results)