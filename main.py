from schema import get_mock_schema
from mistral_client import ask_mistral_for_sql
from guardrails import validate_sql

def main():
    schema = get_mock_schema()
    question = input("Que désirez-vous savoir ? ")
    sql = ask_mistral_for_sql(schema, question)
    print(f"\nSQL généré par Mistral :\n{sql}\n")

    try:
        validate_sql(sql)
        print("La requete SQL est validée avec succès")
    except ValueError as e:
        print(f"Erreur de validation SQL : {e}")

if __name__ == "__main__":
    main()