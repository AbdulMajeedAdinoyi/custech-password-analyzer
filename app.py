# app.py
from flask import Flask, request, jsonify, render_template
from analyzer import score_password

# Create the Flask app and point to templates/static folders
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/", methods=["GET"])
def index():
    """
    Render the main page (templates/index.html).
    """
    return render_template("index.html")

@app.route("/api/score", methods=["POST"])
def api_score():
    """
    Accept JSON: { "password": "..." }
    Return JSON: { score, category, feedback, compromised }
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    pw = data.get("password", "")
    if not isinstance(pw, str):
        return jsonify({"error": "Password must be a string"}), 400

    result = score_password(pw)
    # Breach check is optional and disabled for now
    result["compromised"] = False
    return jsonify(result), 200

@app.route("/health", methods=["GET"])
def health():
    """
    Simple health check endpoint.
    """
    return jsonify({"status": "ok"}), 200

# Basic error handlers for cleaner JSON responses
@app.errorhandler(404)
def not_found(_e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(_e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Debug for local development only
    app.run(host="127.0.0.1", port=5000, debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)