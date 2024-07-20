#!/usr/bin/env python3
"""set expiration date to the session id"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """expiration"""
    def __init__(self) -> None:
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloads the create_session of sessionAUth"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """search for user_id by session_id"""
        # if session_id and self.user_id_by_session_id[session_id]:
        #     if self.session_duration <= 0:
        #         return self.user_id_by_session_id[session_id]['user_id']
        #     date = self.user_id_by_session_id[session_id]['created_at']
        #     duration = timedelta(seconds=self.session_duration)
        #     current_time = datetime.now()
        #     if date:
        #         if date + duration > current_time:
        #             return self.user_id_by_session_id[session_id]['user_id']
        #         return None
        #     return None
        # return None
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
        return None
