#!/usr/bin/python3
"""Index view."""
from api.v1.views import app_views
from flask import jsonify



@app_views.route("/status")
def status():
    """status view."""
    return jsonify({"status":"OK"})
