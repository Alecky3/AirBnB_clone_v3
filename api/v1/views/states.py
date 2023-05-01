#!/usr/bin/python3
"""Defines all view related to State objects."""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states', methods=["GET"])
def get_all_states():
    """Returns all state objects."""
    res = []
    states = storage.all('State')
    for s in states.values():
        res.append(s.to_dict())

    return jsonify(res)
