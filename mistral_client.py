from mistralai.client import Mistral
from config import MISTRAL_API_KEY, MODEL_NAME
from prompt_builder import build_prompt

def ask_mistral_for_sql(schema, question):
    client = Mistral(api_key=MISTRAL_API_KEY)
    prompt = build_prompt(schema, question)
    response = client.chat.complete(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    raw_sql = response.choices[0].message.content.strip()
    return clean_sql(raw_sql)

def clean_sql(raw_sql):
    sql = raw_sql.strip()
    if sql.startswith("```"):
        sql = sql.strip("`")
        sql = sql.replace("sql\n", "", 1).replace("sql\r\n", "", 1)
    return sql.strip()

def ask_mistral_to_explain(question, results):
    """
    Prend la question d'origine + les résultats JSON,
    et retourne une explication en langage naturel.
    """
    client = Mistral(api_key=MISTRAL_API_KEY)

    prompt = f"""Voici une question posée par un utilisateur :
"{question}"

Voici les résultats obtenus (au format JSON) :
{results}

Rédige une réponse courte en français, en langage naturel, qui explique
ces résultats à l'utilisateur de façon claire, comme le ferait un assistant.
Ne mentionne pas le mot "JSON", ne reformule pas la question, va droit au but."""

    response = client.chat.complete(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()