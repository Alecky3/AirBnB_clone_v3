#!/usr/bin/python3
"""main app file."""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """calls storage.close()."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handles 404 http errors."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port)
