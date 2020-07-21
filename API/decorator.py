import jwt

from flask import request, jsonify
from functools import wraps

from my_settings import SECRET_KEY, ALGORITHM

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """로그인 데코레이터

            Header:
                Authorization: 검증이 필요한 토큰
                
        """
        try:
            encoded_token = request.headers["Authorization"]
            decoded_token = jwt.decode(encoded_token, SECRET_KEY, ALGORITHM)
            
            return func(*args, **kwargs, **decoded_token)

        except jwt.exceptions.DecodeError:
            return jsonify(message = "INVALID_TOKEN"), 401
        except KeyError:
            return jsonify(message="INVALID_LOGIN"), 401 
        except Exception as e:
            return jsonify(message=f"{e}"), 500

    return wrapper 

