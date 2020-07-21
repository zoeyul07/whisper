import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pymysql
from flask import Blueprint, jsonify, request

from connections import db_connector
from models import ModelDao
from decorator import login_required

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

@diary_app.route('', methods=['PUT'])
@login_required
def change_public(**kwargs):
    """다이어리 공개 여부 변경 API.

    Headers:
        token

    Args:
        user_id:
        diary_id: 다이어리 id
        status: 공개 여부

    Return:
        None

    Exceptions:
        InternalError: DATABASE가 존재하지 않을 때 발생
        OperationalError: DATABASE 접속이 인가되지 않았을 때 발생
        ProgramingError: SQL syntax가 잘못되었을 때 발생
        IntegrityError: Key의 무결성을 해쳤을 때 발생
        DataError: 컬럼 타입과 매칭되지 않는 값이 DB에 전달되었을 때 발생
        KeyError: 엔드포인트에서 요구하는 키값이 전달되지 않았을 때 발생
    """
    db = None
    try:
        user_id = kwargs['id']

        diaries = request.json['diary_id']

        # Public 상태 변경
        status = request.args['status']
        if status == 'public':
            public = 1
        elif status == 'secret':
            public = 0

        # requset body로 들어온 diary id를 tuple로 변경
        diary_list = []
        for diary in diaries:
            diary_id = diary['id']
            diary_list.append(diary_id)
        diary_tuple = tuple(diary_list)

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        db.begin()
        model_dao.change_diary_public(db, public, diary_tuple, user_id)
        db.commit()
        return (''), 200

    except pymysql.err.InternalError:
        db.rollback()
        return jsonify(message="DATABASE_DOES_NOT_EXIST"), 500
    except pymysql.err.OperationalError:
        db.rollback()
        return jsonify(message="DATABASE_AUTHORIZATION_DENIED"), 500
    except pymysql.err.ProgrammingError:
        db.rollback()
        return jsonify(message="DATABASE_SYNTAX_ERROR"), 500
    except pymysql.err.IntegrityError:
        db.rollback()
        return jsonify(message="FOREIGN_KEY_CONSTRAINT_ERROR"), 500
    except pymysql.err.DataError:
        db.rollback()
        return jsonify(message="DATA_ERROR"), 400
    except KeyError:
        db.rollback()
        return jsonify(message="KEY_ERROR"), 400
    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
