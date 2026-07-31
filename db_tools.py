import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def list_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            rows = cur.fetchall()
            return [row[0] for row in rows]

def describe_table(table_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
            """, (table_name,))
            rows = cur.fetchall()
            return [{"column": r[0], "type": r[1]} for r in rows]

def execute_query(sql):
    from guardrails import is_sql_safe
    if not is_sql_safe(sql):
        return {"error": f"Requete SQL rejetée par les guardrails : {sql}"}
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return [dict(zip(columns, row)) for row in rows]