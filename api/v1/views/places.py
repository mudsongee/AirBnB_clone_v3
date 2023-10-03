#!/usr/bin/python3
"""This module defines the views for Place objects."""
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flasgger import swag_from


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documetation/place/get_place.yml')
def get_places_by_city(city_id):
    """Get list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documetation/place/get_place.yml')
def get_place(place_id):
    """Get a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documetation/place/delete_place.yml')
def delete_place(place_id):
    """Delete a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documetation/place/create_place.yml')
def create_place(city_id):
    """Create a new Place object for a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    name = data.get("name")
    if name is None:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documetation/place/update_place.yml')
def update_place(place_id):
    """Update a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())
