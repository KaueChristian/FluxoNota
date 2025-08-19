from functools import wraps
from flask import request, jsonify
from app.models import User

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = request.headers['Authorization'].split(" ")[1]
            
        if not token:
            return jsonify({'message': 'Token in missing!'}), 401
        
        user = User.query.filter_by(token=token).first()

        if not user:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(user, *args, **kwargs)
    
    return decorated_function

        
