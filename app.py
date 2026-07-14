from flask import Flask, render_template, request, jsonify
from schema import get_mock_schema
from mistral_client import ask_mistral_for_sql, ask_mistral_to_explain
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


@app.route("/api/explain", methods=["POST"])
def explain_results_api():
    data = request.get_json()
    question = data.get("question", "")
    results = data.get("results", [])

    if not question or not results:
        return jsonify({"error": "question ou résultats manquants"}), 400

    explanation = ask_mistral_to_explain(question, results)
    return jsonify({"explanation": explanation}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)