from flask import Flask, jsonify, Response
from analysis_data import CalculateQuarter, QueryData
from API_TEMPLATE import API_RESPONSE
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome!</p>"

@app.route("/api/v1/<ticker>")
def query_basic_info(ticker):
    data = QueryData(str(ticker.upper())).get_basic_info()
    API_RESPONSE["code"] = 200
    API_RESPONSE["success"] = True
    API_RESPONSE["message"] = "Query Successful"
    API_RESPONSE["data"] = data

    # Use json.dumps with sort_keys=False to preserve key order
    response_json = json.dumps(API_RESPONSE, sort_keys=False)

    # Create a Flask Response with the JSON data
    response = Response(response_json, content_type='application/json')

    return response

if __name__ == "__main__":
    app.run(debug=True)