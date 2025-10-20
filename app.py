# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from processor import find_best_trade
from utils import parse_csv_prices
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    # serve frontend index
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/process_csv', methods=['POST'])
def process_csv():
    """
    Accepts multipart/form-data with 'file' (CSV) containing two columns: date,price
    Returns: JSON with processed series and recommended buy/sell
    """
    if 'file' not in request.files:
        return jsonify({"error": "Missing 'file'"}), 400
    f = request.files['file']
    try:
        series = parse_csv_prices(f.stream.read().decode('utf-8'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = find_best_trade(series)
    return jsonify(result)

@app.route('/api/process_json', methods=['POST'])
def process_json():
    """
    Accepts JSON payload:
    { "series": [ {"date":"YYYY-MM-DD","price": 123.45}, ... ] }
    """
    data = request.get_json()
    if not data or 'series' not in data:
        return jsonify({"error": "Missing 'series' in JSON body"}), 400
    series = data['series']
    # Basic validation
    if not isinstance(series, list) or len(series) < 2:
        return jsonify({"error": "series must be a list with at least 2 points"}), 400

    # normalize and validate entries
    cleaned = []
    for p in series:
        if 'price' not in p:
            return jsonify({"error": "each entry must have 'price' and 'date'"}), 400
        try:
            price = float(p['price'])
        except Exception:
            return jsonify({"error": f"invalid price: {p.get('price')}"}), 400
        date = p.get('date', '')
        cleaned.append({"date": date, "price": price})

    result = find_best_trade(cleaned)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
