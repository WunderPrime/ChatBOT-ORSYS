FORBIDDEN_KEYWORDS = [
    "DELETE", "UPDATE", "INSERT", "DROP",
    "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE",
]


def is_sql_safe(sql):
    """
    Vérifie si la requête SQL ne contient pas de mots-clés interdits.
    """
    if sql.strip().upper() == "INVALID":
        return False

    sql_upper = sql.upper()

    if not sql_upper.strip().startswith("SELECT"):
        return False

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            return False

    return True


def validate_sql(sql):
    if not is_sql_safe(sql):
        raise ValueError(f"Requête SQL rejetée par les guardrails : {sql}")