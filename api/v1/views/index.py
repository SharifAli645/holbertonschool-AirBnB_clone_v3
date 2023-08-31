#!/usr/bin/python3
"""A new route"""
from api.v1.views.__init__ import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    dicty = {"amenities": storage.count(Amenity),
             "cities": storage.count(City),
             "places": storage.count(Place),
             "reviews": storage.count(Review),
             "states": storage.count(State),
             "users": storage.count(User)}
    return jsonify(dicty)


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    return jsonify({"status": "OK"})
