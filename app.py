from flask import Flask, jsonify, Response, request
from analysis_data import CalculateQuarter, QueryData
from API_TEMPLATE import api_response
import json

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<p>Welcome!</p>"


@app.route("/api/v1/basic", methods=["POST"])
def query_basic_post():
    # Get Incoming POST Message
    request_data = request.json
    ticker = request_data["ticker_code"]

    data = QueryData(ticker.upper()).get_basic_info()

    API_RESPONSE = api_response(200, True, "Query Successful", data)

    # Use json.dumps with sort_keys=False to preserve key order
    response_json = json.dumps(API_RESPONSE, sort_keys=False)

    # Create a Flask Response with the JSON data
    response = Response(response_json, content_type='application/json')

    return response


@app.route("/api/v1/list-quartal", methods=["POST"])
def list_report():
    # Get Incoming POST Message
    request_data = request.json
    ticker = request_data["ticker_code"]
    sheet_overview = QueryData(ticker)

    data = sheet_overview.get_balance_sheet_quarter()['asOfDate'].dt.strftime("%Y-%m-%d").tolist()
    
    API_RESPONSE = api_response(200, True, "Query Successful", data)

    # Use json.dumps with sort_keys=False to preserve key order
    response_json = json.dumps(API_RESPONSE, sort_keys=False)

    # Create a Flask Response with the JSON data
    response = Response(response_json, content_type='application/json')

    return response

@app.route("/api/v1/quartal-fundamental/", methods=["POST"])
def report_quartal():
    # Get Incoming POST Message
    request_data = request.json
    ticker = request_data["ticker_code"]
    date_time = request_data["date_time"]

    data = CalculateQuarter(ticker.upper(), date_time).output()
    
    API_RESPONSE = api_response(200, True, "Query Successful", data)

    # Use json.dumps with sort_keys=False to preserve key order
    response_json = json.dumps(API_RESPONSE, sort_keys=False)

    # Create a Flask Response with the JSON data
    response = Response(response_json, content_type='application/json')

    return response

if __name__ == "__main__":
    app.run(debug=True)