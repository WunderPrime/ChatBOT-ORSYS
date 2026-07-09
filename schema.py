import psycopg2

def get_schema(conn):
    """Return a dict mapping table_name -> list of (column_name, data_type)."""
    schema = {}
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
            """
        )
        rows = cursor.fetchall()

    for table_name, column_name, data_type in rows:
        schema.setdefault(table_name, []).append((column_name))

    schema_text = ""
    for table_name, columns in schema.items():
        schema_text += f"{table_name}({', '.join(columns)})\n"
    return schema_text

def get_mock_schema():
    """Return a mock schema for testing"""
    return """users(id, name, email)"""