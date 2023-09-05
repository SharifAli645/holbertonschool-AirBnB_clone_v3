#!/usr/bin/python3
"""Module that contains view of state"""
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def place_city_id(city_id):
    """Retrieves the list of all Place objects of a city"""
    obj_state = storage.get(City, city_id)
    if not obj_state:
        abort(404)
    obj = storage.all(Place).values()
    lis = [u.to_dict() for u in obj if u.city_id == city_id]
    return jsonify(lis)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def place_id(place_id):
    """Retrieves a Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def place_id_delete(place_id):
    """Deletes a Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def place_post(city_id):
    """Creates a Place"""
    data = request.get_json()
    if not storage.get(City, city_id):
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get(User, data.get('user_id')):
        abort(404)
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_obj = City(name=data.get('name'), city_id=city_id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def place_put(place_id):
    """Updates a Place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    s1 = 'created_at'
    s2 = 'updated_at'
    ci = 'city_id'
    ui = 'user_id'
    for k, v in data.items():
        if k != 'id' or k != s1 or k != s2 or k != ci or k != ui:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
