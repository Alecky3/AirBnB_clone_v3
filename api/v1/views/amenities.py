#!/usr/bin/python3
"""Defines all view related to Amenity objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """Returns all amenity objects."""
    res = []
    amenities = storage.all('Amenity')
    for s in amenities.values():
        res.append(s.to_dict())

    return jsonify(res)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_byid(amenity_id):
    """Retuns a amenity by its id."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a amenity object."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities/", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Updates a amenity object."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)

    amenity.save()
    return jsonify(amenity.to_dict())
