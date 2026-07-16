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

def get_schema_list():
    """Retourne chaque table comme un élément séparé de liste"""
    return [
        "users(id, name, email)",
        "commandes(id, user_id, montant, date_commande)",
        "produits(id, nom, prix, stock)",
        "factures(id, commande_id, montant_ttc, date_facture)",
        "reclamations(id, user_id, sujet, statut)",
    ]