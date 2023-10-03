#!/usr/bin/python3
"""This module defines the views for Review objects."""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flasgger import swag_from


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml')
def get_reviews(place_id):
    """Get list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml')
def get_review(review_id):
    """Get a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/reviews/delete_review.yml')
def delete_review(review_id):
    """Delete a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/reviews/create_review.yml')
def create_review(place_id):
    """Create a new Review object for a Place"""
    place = storage.get(Place, place_id)
    if place is None:
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

    text = data.get("text")
    if text is None:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/reviews/update_review.yml')
def update_review(review_id):
    """Update a Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in [
            'id', 'user_id',
            'place_id',
            'created_at',
            'updated_at'
        ]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())

# #!/usr/bin/python3
# """This module defines the views for Review objects."""
# from api.v1.views import app_views
# from flask import jsonify, abort, request
# from models import storage
# from models.place import Place
# from models.review import Review
# from models.user import User
# from flasgger.utils import swag_from


# @app_views.route('/places/<place_id>/reviews', methods=['GET'],
#                  strict_slashes=False)
# def get_reviews(place_id):
#     """Get list of all Review objects of a Place"""
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)
#     reviews = [review.to_dict() for review in place.reviews]
#     return jsonify(reviews)


# @app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
# def get_review(review_id):
#     """Get a Review object by its ID"""
#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)
#     return jsonify(review.to_dict())


# @app_views.route('/reviews/<review_id>', methods=['DELETE'],
#                  strict_slashes=False)
# def delete_review(review_id):
#     """Delete a Review object by its ID"""
#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)
#     storage.delete(review)
#     storage.save()
#     return jsonify({})


# @app_views.route('/places/<place_id>/reviews', methods=['POST'],
#                  strict_slashes=False)
# def create_review(place_id):
#     """Create a new Review object for a Place"""
#     place = storage.get(Place, place_id)
#     if place is None:
#         abort(404)

#     data = request.get_json()
#     if data is None:
#         return jsonify({"error": "Not a JSON"}), 400

#     user_id = data.get("user_id")
#     if user_id is None:
#         return jsonify({"error": "Missing user_id"}), 400

#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)

#     text = data.get("text")
#     if text is None:
#         return jsonify({"error": "Missing text"}), 400

#     new_review = Review(**data)
#     new_review.place_id = place_id
#     new_review.save()
#     return jsonify(new_review.to_dict()), 201


# @app_views.route('/reviews/<review_id>', methods=['PUT'],
#                  strict_slashes=False)
# def update_review(review_id):
#     """Update a Review object by its ID"""
#     review = storage.get(Review, review_id)
#     if review is None:
#         abort(404)

#     data = request.get_json()
#     if data is None:
#         return jsonify({"error": "Not a JSON"}), 400

#     for key, value in data.items():
#         if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
#             setattr(review, key, value)

#     review.save()
#     return jsonify(review.to_dict())
