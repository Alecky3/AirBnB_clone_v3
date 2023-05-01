#!/usr/bin/python3
"""Defines all view related to State objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def get_all_states():
    """Returns all state objects."""
    res = []
    states = storage.all('State')
    for s in states.values():
        res.append(s.to_dict())

    return jsonify(res)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state_byid(state_id):
    """Retuns a state by its id."""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state object."""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a state object."""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)

    state.save()
    return jsonify(state.to_dict())
