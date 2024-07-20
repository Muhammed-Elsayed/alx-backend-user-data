#!/usr/bin/env python3
"""all routes for session authentication"""
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = make_response(jsonify(user[0].to_json()))
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """logout"""
    from api.v1.app import auth
    res = auth.destroy_session(request)
    if res:
        return jsonify({}), 200
    abort(404)
