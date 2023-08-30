from flask import Flask, jsonify
from analysis_data import CalculateQuarter
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome!</p>"

@app.route("/api/bmri")
def query():
    data = CalculateQuarter("BMRI", "2023-03-31").output()
    pretty_json = json.dumps(data, indent=4)
    return '<pre>{}</pre>'.format(pretty_json)

if __name__ == "__main__":
    app.run(debug=True)