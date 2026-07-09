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