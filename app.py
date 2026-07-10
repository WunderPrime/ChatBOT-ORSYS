from flask import Flask, render_template, request, jsonify
from schema import get_mock_schema
from mistral_client import ask_mistral_for_sql
from guardrails import is_sql_safe

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/generate-sql", methods=["POST"])
def generate_sql_api():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "question manquante"}), 400

    schema = get_mock_schema()
    sql = ask_mistral_for_sql(schema, question)

    if is_sql_safe(sql):
        return jsonify({"sql": sql}), 200
    else:
        return jsonify({"error": f"Requête rejetée par les guardrails : {sql}"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)