#!/usr/bin/python3
"""Module that contains view of state"""
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    obj = storage.all(State).values()
    lis = [element.to_dict() for element in obj]
    return jsonify(lis)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def state_id_delete(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_post():
    """Creates a State"""
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_obj = State(name=data.get('name'))
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def state_put(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
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
