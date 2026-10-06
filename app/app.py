import os
from flask import Flask, jsonify

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "unknown")
FORCE_FAIL = os.getenv("FORCE_FAIL", "false").lower() == "true"

@app.route("/")
def home():
    return jsonify({"version": VERSION, "status": "ok"})

@app.route("/health")
def health():
    # FORCE_FAIL=true simulates a broken deployment for rollback testing
    if FORCE_FAIL:
        return jsonify({"status": "unhealthy", "version": VERSION}), 500
    return jsonify({"status": "healthy", "version": VERSION}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
