from flask import Flask, render_template, request
from schema import get_mock_schema
from mistral_client import ask_mistral_for_sql
from guardrails import is_sql_safe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    sql_result = None
    error = None

    if request.method == "POST":
        question = request.form["question"]
        schema = get_mock_schema()
        sql = ask_mistral_for_sql(schema, question)

        if is_sql_safe(sql):
            sql_result = sql
        else:
            error = f"Requete SQL rejetée : {sql}"

    return render_template("index.html", question=question, sql_result=sql_result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)