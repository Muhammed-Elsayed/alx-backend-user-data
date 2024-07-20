#!/usr/bin/env python3
"""Auth class for handling authentication with the API."""
from flask import request
from os import getenv
import re
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """needs authentication or not"""
        if path is None or excluded_paths is None \
                or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for pth in excluded_paths:
            if pth[-1] == '*':
                pattern = fr'{pth[0:-1]}.*'
                if re.match(pattern, path):
                    return False
            else:
                if pth == path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    User = TypeVar('User')

    def current_user(self, request=None) -> User:
        """current user"""
        return None

    def session_cookie(self, request=None):
        """session cookie"""
        if request:
            return request.cookies.get(getenv('SESSION_NAME'), None)
        return None
