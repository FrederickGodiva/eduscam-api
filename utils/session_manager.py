import random
from config.settings import settings

class SessionManager:
    def __init__(self):
        self.sessions = {}
        
    def create_session(self, session_id, phone_number):
        self.sessions[session_id] = {
            'phone_number': phone_number,
            'turn_counter': 0,
            'conversation_history': [],
            'is_simulation_revealed': False,
            'scam_type': random.choice(settings.SCAM_TYPES),
            'user_flag': None
        }
        return self.sessions[session_id]

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def update_session(self, session_id, user_message, bot_message, user_flag=None):
        session = self.sessions[session_id]
        session['conversation_history'].extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": bot_message}
        ])
        session['turn_counter'] += 1
        if user_flag:
            session['user_flag'] = user_flag
