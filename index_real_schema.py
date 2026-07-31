import db_tools
from vector_store_langchain import index_schema

def build_schema_description():
    descriptions = []
    for table_name in db_tools.list_tables():
        columns = db_tools.describe_table(table_name)
        columns_text = ", ".join(f"{c['column']} ({c['type']})" for c in columns)
        descriptions.append(f"{table_name}({columns_text})")
    return descriptions


if __name__ == "__main__":
    descriptions = build_schema_description()
    index_schema(descriptions)
    print(f"{len(descriptions)} tables indexées:")
    for d in descriptions:
        print(f"- {d}")