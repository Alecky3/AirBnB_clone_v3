#!/usr/bin/python3
"""Defines all view related to Place objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models import storage


@app_views.route('/places', methods=["GET"], strict_slashes=False)
def get_all_places():
    """Returns all place objects."""
    res = []
    places = storage.all('Place')
    for s in places.values():
        res.append(s.to_dict())

    return jsonify(res)


@app_views.route("/places/<state_id>", methods=["GET"])
def get_place_byid(state_id):
    """Retuns a place by its id."""
    place = storage.get('Place', state_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<state_id>", methods=['DELETE'])
def delete_place(state_id):
    """Deletes a place object."""
    place = storage.get('Place', state_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/", methods=["POST"], strict_slashes=False)
def create_place():
    """Creates a Place object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    place = Place(**request.get_json())
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<state_id>", methods=["PUT"])
def update_place(state_id):
    """Updates a place object."""
    place = storage.get('Place', state_id)
    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(place, k, v)

    place.save()
    return jsonify(place.to_dict())
