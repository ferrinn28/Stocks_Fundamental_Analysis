from flask import Flask, jsonify
from analysis_data import CalculateQuarter, QueryData
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome!</p>"

@app.route("/api/<ticker>")
def query_basic_info(ticker):
    data = QueryData(str(ticker.upper())).get_basic_info()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)