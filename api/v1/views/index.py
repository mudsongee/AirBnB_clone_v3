#!/usr/bin/python3
"""
This module implement a rule that returns
the status of the application Done
"""
from flask import jsonify, request
import models
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def view_status():
    """View function that return a json message"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats", strict_slashes=False)
def view_stats():
    """View function that retrieves the number of each object by type."""
    if request.method == 'GET':
        response = {}
    stats = {
        "amenities": models.storage.count('Amenity'),
        "cities": models.storage.count('City'),
        "places": models.storage.count('Place'),
        "reviews": models.storage.count('Review'),
        "states": models.storage.count('State'),
        "users": models.storage.count('User'),

    }
    for key, value in stats.items():
            response[value] = storage.count(key)
    return jsonify(stats)
