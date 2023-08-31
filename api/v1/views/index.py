#!/usr/bin/python3
"""A new route"""
from api.v1.views.__init__ import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
