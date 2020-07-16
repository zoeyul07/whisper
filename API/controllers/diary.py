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
        return jsonify(emotion=f"{data}"), 200
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
        return jsonify(question=f"{data}"), 200
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

