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

        series_id = model_dao.search_series(db, user_id, name)

        # 시리즈 중복 확인
        if series_id:
            return jsonify(message="EXIST_SERIES"), 400

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

@series_app.route('', methods=['GET'])
def find_user_series():
    """ user별 시리즈 조회

    """
    db = None
    try:
        user_id = 1

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        series_data = model_dao.my_series(db, user_id)
        data = [
            {
                "id": series['id'],
                "name": series['name'],
                "count": model_dao.count_series_diary(db, user_id, series['id'])
            }for series in series_data ]

        return jsonify(data), 200

    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@series_app.route('/<int:series_id>', methods=['PUT'])
def change_series_name(series_id):
    """시리즈 이름 변경 API

    """
    try:
        db = None

        user_id = 1
        name = request.json['name']

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        db.begin()
        model_dao.update_series_name(db, name, series_id)
        db.commit()
        return (''), 200

    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@series_app.route('/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    """시리즈 삭제하는 API

    """
    try:
        db = None

        user_id = 1

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        db.begin()
        model_dao.delete_series_from_db(db, series_id, user_id)
        model_dao.delete_series_from_diaries(db, series_id, user_id)
        db.commit()
        return (''), 200

    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@series_app.route('diary/<int:series_id>', methods=['GET'])
def diaries_series(series_id):
    """시리즈별 다이어리 보여주는 API

    """
    try:
        db = None

        user_id = 1

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        diaries = model_dao.search_diaries_in_series(db, series_id, user_id)
        diary=[
            {
                "diary_id": data['id'],
                "emotion_id": data['emotion_id'],
                "image_url":data['image_url'],
                "color":data['color'],
                "summary":data['summary'],
                "like": True if data['is_deleted'] == 0 else False,
                "is_public": True if data['public'] == 1 else False,
                "count":model_dao.count_likes(db, data['id'])
            }for data in diaries]

        return jsonify(diary), 200
    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
