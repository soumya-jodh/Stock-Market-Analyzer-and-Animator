# backend/app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from processor import find_best_trade
from utils import parse_csv_prices
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    # serve frontend index
    return render_template('index.html')

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
        # The CSV is read and decoded, then parsed by the utility function
        series = parse_csv_prices(f.stream.read().decode('utf-8'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = find_best_trade(series)
    return jsonify(result)

# The /api/process_json route is completely removed as requested.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)