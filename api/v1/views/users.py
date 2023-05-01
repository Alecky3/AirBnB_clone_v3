#!/usr/bin/python3
"""Defines all view related to User objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_all_users():
    """Returns all user objects."""
    res = []
    users = storage.all('User')
    for s in users.values():
        res.append(s.to_dict())

    return jsonify(res)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user_byid(user_id):
    """Retuns a user by its id."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user object."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a user object."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict())
