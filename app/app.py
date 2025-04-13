from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


log_dir = '/app/logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return "Welcome to the custom app"

@app.route('/status')
def status():
    return jsonify({"status": "ok"})

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    app.logger.info(data['message'])
    return jsonify({"status": "logged"})

@app.route('/logs')
def get_logs():
    try:
        with open(log_file, 'r') as f:
            logs = f.read()
        return logs
    except FileNotFoundError:
        return "No logs found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 