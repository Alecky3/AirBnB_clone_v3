#!/usr/bin/python3
"""Defines all view related to City objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.city import City
from models import storage


@app_views.route('/cities', methods=["GET"], strict_slashes=False)
def get_all_cities():
    """Returns all city objects."""
    res = []
    cities = storage.all('City')
    for s in cities.values():
        res.append(s.to_dict())

    return jsonify(res)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_byid(city_id):
    """Retuns a city by its id."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/", methods=["POST"], strict_slashes=False)
def create_city():
    """Creates a City object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = City(**request.get_json())
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a city object."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)

    city.save()
    return jsonify(city.to_dict())
