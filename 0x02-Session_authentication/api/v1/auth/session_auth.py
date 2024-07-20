#!/usr/bin/env python3
"""session authentication with sessionAuth class"""
from .auth import Auth
from uuid import uuid4
from os import getenv
from models.user import User


class SessionAuth(Auth):
    """Session Authentication Class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id for the given user"""
        if user_id is None or type(user_id) is not str:
            return None
        # Generate a unique session id
        session_id = str(uuid4())  # Create a random UUID
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user_id associated with this session_id"""
        if session_id and type(session_id) is str:
            return self.user_id_by_session_id.get(session_id, None)
        return None

    def current_user(self, request=None):
        """Get the currently logged in user from
        the request object's session_id"""
        try:
            session_id = request.cookies.get(getenv('SESSION_NAME'), None)
            user_id = self.user_id_for_session_id(session_id)
            return User.get(user_id)
        except Exception:
            return None

    def destroy_session(self, request=None):
        """destroy the current session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
