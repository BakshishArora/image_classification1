from functools import wraps
from flask import request, jsonify
from app.service.auth import Authorize
from app.service.image_service import generate_return_dictionary

def protect_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify(generate_return_dictionary(403, "Authorization header is missing."))
        
        parts = auth_header.split()
        if len(parts) !=2 or parts[0].lower()!='bearer':
            return jsonify(generate_return_dictionary(403, "Invalid Authorization Header"))
        
        token = parts[1]
        result = Authorize.decrypt(token)

        if "error" in result:
            return jsonify(generate_return_dictionary(403, "Invalid Token"))
        
        return f(*args,**kwargs)
    return decorated_function

        
