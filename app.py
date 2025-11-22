import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from places import get_top_50_attractions

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Read SerpAPI key
SERPAPI_KEY = os.environ.get(
    "SERPAPI_KEY"
)

@app.route("/")
def index():
    # serve index.html from same directory as app.py
    return send_from_directory(".", "index.html")

@app.route("/api/places")
def places():
    city = request.args.get("city")
    tag = request.args.get("tag", "tourist attractions")

    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        places_list = get_top_50_attractions(city, SERPAPI_KEY, tag)
        return jsonify({"places": places_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Render will use gunicorn:app:app, so no need to run here
if __name__ == "__main__":
    app.run(debug=True, port=5000)
