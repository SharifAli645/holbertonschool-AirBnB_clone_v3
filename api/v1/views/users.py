#!/usr/bin/python3
"""Module that contains view of state"""
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
    """Retrieves the list of all User objects"""
    obj = storage.all(User).values()
    lis = [element.to_dict() for element in obj]
    return jsonify(lis)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user_id(user_id):
    """Retrieves a User object"""
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def user_id_delete(user_id):
    """Deletes a User object"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def users_post():
    """Creates a User"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    new_obj = User(email=data.get('email'),
                   password=data.get('password'))
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def user_put(state_id):
    """Updates a User object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    s1 = 'created_at'
    s2 = 'updated_at'
    for k, v in data.items():
        if k != 'id' or k != s1 or k != s2 or k != 'email':
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
