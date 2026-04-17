# app/app.py
from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "service": "devops-lab",
        "hostname": socket.gethostname(),
        "version": os.environ.get("APP_VERSION", "1.0.0"),
    })


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)