import json
from mistralai.client import Mistral
from config import MISTRAL_API_KEY, MODEL_NAME
import db_tools
from vector_store_langchain import retrieve_relevant_tables

client = Mistral(api_key=MISTRAL_API_KEY)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_tables",
            "description": "Liste toutes les tables disponibles dans la base de données",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "describe_table",
            "description": "Retourne les colonnes et types d'une table donnée",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Nom exact de la table"}
                },
                "required": ["table_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_query",
            "description": "Exécute une requête SQL SELECT en lecture seule et retourne les résultats",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "Requête SQL SELECT uniquement"}
                },
                "required": ["sql"],
            },
        },
    },
    {
    "type": "function",
    "function": {
        "name": "search_relevant_tables",
        "description": "Recherche les tables les plus pertinentes pour une question donnée, par similarité sémantique. À utiliser EN PREMIER avant d'explorer les tables une par une.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "La question de l'utilisateur"}
            },
            "required": ["question"],
        },
    },
},
]

AVAILABLE_FUNCTIONS = {
    "list_tables": lambda **kwargs: db_tools.list_tables(),
    "describe_table": lambda **kwargs: db_tools.describe_table(kwargs["table_name"]),
    "search_relevant_tables": lambda **kwargs: retrieve_relevant_tables(kwargs["question"]),
    "execute_query": lambda **kwargs: db_tools.execute_query(kwargs["sql"]),
}


def run_agent(question, max_steps=5):
    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un agent qui répond à des questions sur une base de données PostgreSQL. "
                "Utilise TOUJOURS 'search_relevant_tables' en premier pour trouver les tables pertinentes. "
                "Ensuite, utilise 'describe_table' uniquement sur les tables trouvées pour connaître leurs colonnes exactes. "
                "Exécute enfin une requête SELECT uniquement, via 'execute_query'. "
                "Ne devine jamais un nom de colonne : vérifie toujours avec describe_table avant."
            ),
        },
        {"role": "user", "content": question},
    ]

    last_sql = None
    last_results = None
    last_error = None

    for _ in range(max_steps):
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return {
                "sql": last_sql,
                "results": last_results,
                "explanation": message.content,
                "error": last_error,
            }

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            result = AVAILABLE_FUNCTIONS[function_name](**arguments)

            # On capture le SQL et les résultats quand l'outil execute_query est appelé
            if function_name == "execute_query":
                last_sql = arguments.get("sql")
                if isinstance(result, dict) and "error" in result:
                    last_error = result["error"]
                else:
                    last_results = result

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result, default=str),
            })

    return {
        "sql": last_sql,
        "results": last_results,
        "explanation": "Aucune réponse finale générée après le nombre maximum d'étapes.",
        "error": last_error,
    }