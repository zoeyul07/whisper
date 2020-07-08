import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pymysql
from flask import Blueprint, request, jsonify

from connections import db_connector
from models import ModelDao

series_app = Blueprint("series_app", __name__)
model_dao = ModelDao()

@series_app.route('', methods=['POST'])
def new_series():
    """새로운 시리즈 생성 API

    """

    db = None
    try:
        # user_id = 토큰에서 받아온 user_id
        user_id = 1
        name = request.json['name']

        db = db_connector()
        # db 에러처리
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        # db에 값 추가
        db.begin()
        model_dao.insert_series(db, user_id, name)
        db.commit()

        return (''), 200

    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
