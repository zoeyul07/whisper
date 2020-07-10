import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import jwt
import pymysql
from flask import Blueprint, jsonify, request

from connections import db_connector
from my_settings import SECRET_KEY, ALGORITHM
from models import ModelDao

user_app = Blueprint('user', __name__)
model_dao = ModelDao()

@user_app.route('/kakao', methods=['POST'])
def kakao():
    """ kakao 로그인 API

    """
    db = None
    try:
        token = request.headers['Authorization']
        nickname = request.get_json(silent=True).get('nickname', None)

        if not token:
            return jsonify(message="TOKEN_DOES_NOT_EXIST"), 400

        data = request.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        kakao_id = data.json()['kakao_id']

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        kakao_user = model_dao.search_kakao_user(db, kakao_id)
        # 가입된 계정인 경우 로그인 진행
        if kakao_user:
            token = jwt.encode(kakao_user, SECRET_KEY, ALGORITHM)
            return Jsonify(token=token.decode('utf-8'), nickname=nickname), 200
        # 가입되어있지 않은 계정인 경우 회원가입 진행
        elif kakao_user is None:
            db.begin()
            social_id = model_dao.insert_kakao_user(db, kakao_id)
            if nickname:
                kakao_user = model_dao.insert_kakao_into_user(db, social_id, nickname)
                token = jwt.encode(kakao_user, SECRET_KEY, ALGORITHM)
                return Jsonify(token=token.decode('utf-8'), nickname=nickname), 200
            # 닉네임 입력하지 않은 경우 에러처리
            elif nickname is None:
                return jsonify(message="DATA_ERROR"), 400
            db.commit()

    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
