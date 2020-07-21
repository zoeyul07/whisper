import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pymysql
from flask import Blueprint, jsonify, request

from connections import db_connector
from models import ModelDao

diary_app = Blueprint("diary", __name__)
model_dao = ModelDao()

#이모티콘 정보 보내주기
@diary_app.route('/emotion', methods=['GET'])
def emotion():
    db = None
    try:
        db = db_connector()

        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = model_dao.search_emotion(db)
        return jsonify(emotion=data), 200
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

#질문 전달
@diary_app.route('/question', methods=['GET'])
def question():
    db = None
    try:
        db = db_connector()

        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = model_dao.search_question(db)
        return jsonify(question=data), 200
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

# 다른 사람 다이어리 모두 보기
@diary_app.route('/<int:user_id>', methods=['GET'])
def other_person_diary(user_id):
    db = None
    try:
        db = db_connector()

        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data_list = model_dao.other_person_diary(db, user_id)

        other_person = [
            {
                "nickname":data['nickname'],
                "diary_id":data['id'],
                "emotion_id":data['emotion_id'],
                "image_url":data['image_url'],
                "color":data['color'],
                "summary":data['summary'],
                "like":True if data['is_deleted'] == 0 else False,
                "count":model_dao.count_likes(db, data['id'])
            }for data in data_list
        ]
        return jsonify(diary=other_person),200
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
