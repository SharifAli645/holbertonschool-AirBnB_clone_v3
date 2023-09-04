#!/usr/bin/python3
"""Module that contains view of state"""
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def city_state(state_id):
    """Retrieves the list of all City objects of a State"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)
    obj = storage.all(City).values()
    lis = [u.to_dict() for u in obj if u.state_id == state_id]
    return jsonify(lis)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_id(city_id):
    """Retrieves a City object"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def city_id_delete(city_id):
    """Deletes a City object"""
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def city_post(state_id):
    """Creates a State"""
    data = request.get_json()
    if not storage.get(State, state_id):
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_obj = City(name=data.get('name'), state_id=state_id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def city_put(city_id):
    """Updates a State object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in data.items():
        if k != 'id' or k != 'created_at' or k != 'updated_at':
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
