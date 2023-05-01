#!/usr/bin/python3
"""Index view."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }


@app_views.route("/status")
def status():
    """status view."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Stats view that returns the count of every object in db."""
    res = {}
    for k, v in classes.items():
        res[k] = storage.count(v)

    return jsonify(res)
