from flask import Flask, render_template, request, jsonify
from schema import get_mock_schema, get_schema_list
from mistral_client import ask_mistral_for_sql, ask_mistral_to_explain
from guardrails import is_sql_safe
from vector_store import index_schema, retrieve_relevant_tables
from agent import run_agent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

index_schema(get_schema_list())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/agent-ask", methods=["POST"])
def agent_ask_api():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "question manquante"}), 400

    result = run_agent(question)
    if result.get("error"):
        return jsonify({"error": result["error"]}), 400

    return jsonify({"sql": result["sql"],"results": result["results"], "explanation": result["explanation"]}), 200


@app.route("/api/generate-sql", methods=["POST"])
def generate_sql_api():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "question manquante"}), 400

    relevant_tables = retrieve_relevant_tables(question, top_k=3)
    schema = "\n".join(relevant_tables)
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
    app.run(host="0.0.0.0", port=5000, debug=True)