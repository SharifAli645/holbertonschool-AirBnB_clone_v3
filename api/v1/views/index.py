#!/usr/bin/python3
"""A new route"""
from api.v1.views import app_views
import json

@app_views.route('/status/', strict_slashes=False, methods=['GET'])
def status():
    return json.dumps({"status": "OK"})
