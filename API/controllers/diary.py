import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import pymysql
from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError

from datetime import datetime
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
def other_person_diary(**kwargs):
    db = None
    try:

        users_id = kwargs['id']

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
                "like":True if model_dao.search_is_like(db, users_id, data['id']) == 1 else False,
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

@diary_app.route('', methods=['GET'])
#@login_required
def select_all_diaries(**kwargs):
    """
    모든 다이어리 보기

    ---주석 지우면 안되요!!---
    토큰값 없어서 임시로 주석 달아 놓음.

    """
    db = None
    try:
        #user_id = kwargs['id']

        # pagination 조건 생성
        filter_dict = {}
        filter_dict['limit'] = request.args.get('limit', 10, int)
        filter_dict['offset'] = request.args.get('offset', 0, int)

        filter_dict['emotion'] = request.args.getlist('emotion',int)
        filter_dict['startdate'] = request.args.get('startdate')
        filter_dict['enddate'] = request.args.get('enddate', datetime.today(), str)

        filter_dict['pop']

        db =db_connector()

        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        all_diary_list = model_dao.search_all_diaries(db, filter_dict)
        #like_count = model_dao.search_is_like(db, user_id)

        all_diary = [
            {
                "nickname":diary['nickname'],
                "diary_id":diary['id'],
                "emotion_id":diary['emotion_id'],
                "image_url":diary['image_url'],
                "color":diary['color'],
                "summary":diary['summary'],
                #"like":True if model_dao.search_is_like(db, user_id, diary['id']) == 1 else False,
                "count":model_dao.count_likes(db, diary['id'])
            }for diary in all_diary_list
        ]
        return jsonify(diary=all_diary),200

    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@diary_app.route('', methods=['POST'])
@login_required
def create_diary(**kwargs):
    """새 다이어리 생성"""
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json()
        db.begin()
        diary = model_dao.insert_diary(
                db,
                kwargs['id'],
                data['emotion_id'],
                data['contents'],
                data['summary'],
                data['is_completed'],
                data['public'],
                data['series_id']
                )
        db.commit()
        return '', 200

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

@diary_app.route('/<int:diary_id>', methods=['GET'])
@login_required
def select_diary(**kwargs):
    """다이어리 가져오기"""
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        diary = model_dao.select_diary(db, kwargs['id'], kwargs['diary_id'])
        data = {
            'emotion_id': diary['emotion_id'],
            'series_id': diary['series_id'],
            'contents': diary['contents'],
            'summary': diary['summary'],
            'is_completed': diary['is_completed'],
            'public': diary['public']
            }
        return jsonify(data=data), 200

    except pymysql.err.InternalError:
        return jsonify(message="DATABASE_DOES_NOT_EXIST"), 500
    except pymysql.err.OperationalError:
        return jsonify(message="DATABASE_AUTHORIZATION_DENIED"), 500
    except pymysql.err.ProgrammingError:
        return jsonify(message="DATABASE_SYNTAX_ERROR"), 500
    except pymysql.err.IntegrityError:
        return jsonify(message="FOREIGN_KEY_CONSTRAINT_ERROR"), 500
    except pymysql.err.DataError:
        return jsonify(message="DATA_ERROR"), 400
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@diary_app.route('/<int:diary_id>', methods=['PUT'])
@login_required
def modify_diary(**kwargs):
    """다이어리 수정"""
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json()
        db.begin()
        model_dao.update_diary(
                db,
                data['emotion_id'],
                data['series_id'],
                data['contents'],
                data['summary'],
                data['is_completed'],
                data['public'],
                kwargs['id'],
                kwargs['diary_id']
                )
        db.commit()
        return '', 200

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

@diary_app.route('/<int:diary_id>', methods=['DELETE'])
@login_required
def delete_diary(**kwargs):
    """다이어리 삭제"""
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        db.begin()
        model_dao.delete_diary(db, kwargs['id'], kwargs['diary_id'])
        db.commit()
        return '', 200

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
    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

@diary_app.route('/<int:diary_id>/like', methods=['POST'])
@login_required
def like_diary(**kwargs):
    """다이어리 좋아요"""
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        user_id = kwargs['id']
        diary_id = kwargs['diary_id']
        liked_diary = model_dao.search_id_like(db, user_id, diary_id)

        db.begin()
        if liked_diary:
            model_dao.delete_liked_diary(db, user_id, diary_id)
            return jsonify(message=False), 200

        model_dao.like_diary(db, user_id, diary_id)
        db.commit()
        return jsonify(message=True), 200

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
    except Exception as e:
        db.rollback()
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()
