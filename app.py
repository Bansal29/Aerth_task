from flask import Flask, render_template, jsonify
from selenium_script import fetch_trending_topics

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    record = fetch_trending_topics()
    return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)
