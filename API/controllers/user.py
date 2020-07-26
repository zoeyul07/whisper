import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

import jwt
import pymysql
import bcrypt
import requests
import random

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from connections import db_connector
from my_settings import SECRET_KEY, ALGORITHM
from models import ModelDao
from decorator import login_required
from string import punctuation, ascii_letters, digits
from send_email  import send_email

user_app = Blueprint('user', __name__)
model_dao = ModelDao()

@user_app.route('/kakao', methods=['POST'])
def kakao():
    """kakao 로그인 API.

    Header:
        Authorizaion

    Args:
        nickname: 사용자의 닉네임
        Kakao_id: 카카오톡 소셜 아이디

    Returns:
        {
            token: JWT_TOKEN,
            nickname: 닉네임
        }, http status code

    Exceptions:
        InternalError: DATABASE가 존재하지 않을 때 발생
        OperationalError: DATABASE 접속이 인가되지 않았을 때 발생
        ProgramingError: SQL syntax가 잘못되었을 때 발생
        IntegrityError: Key의 무결성을 해쳤을 때 발생
        DataError: 컬럼 타입과 매칭되지 않는 값이 DB에 전달되었을 때 발생
    """
    db = None
    try:
        access_token = request.headers['Authorization']
        nickname = request.get_json(silent=True)
        if not access_token:
            return jsonify(message="TOKEN_DOES_NOT_EXIST"), 400

        data = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {access_token}'})
        kakao_id = data.json()['id']

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        kakao_user = model_dao.search_kakao_user(db, kakao_id)
        # 가입된 계정인 경우 로그인 진행
        if kakao_user:
            nickname = kakao_user['nickname']
            token = jwt.encode(kakao_user, SECRET_KEY, ALGORITHM)
            return jsonify(token=token.decode('utf-8'), nickname=nickname, message="SIGN_IN_COMPLETE"), 200

        # 가입되어있지 않은 계정인 경우 회원가입 진행
        elif kakao_user is None:
            # 닉네임 입력하지 않은 경우 에러처리
            if nickname is None:
                return jsonify(message="DATA_ERROR"), 400

            db.begin()
            social_id = model_dao.insert_kakao_user(db, kakao_id)
            nickname = nickname['nickname']
            kakao_user = model_dao.insert_kakao_into_user(db, social_id, nickname)
            token = jwt.encode({"id":kakao_user}, SECRET_KEY, ALGORITHM)
            db.commit()
            return jsonify(token=token.decode('utf-8'), nickname=nickname, message="SIGN_UP_COMPLETE"), 200

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

@user_app.route('/sign-up', methods=['POST'])
def sign_up():
    """이메일 회원가입

        Args:
            email : 사용자의 이메일
            nickname : 사용자의 닉네임
            password : 사용자의 비밀번호
    """
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json
        email = model_dao.search_email(db, data['email'])
        if email:
            return jsonify(message="EMAIL_EXIST"), 400

        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        db.begin()
        model_dao.create_user(db, data['email'], data['password'], data['nickname'])
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

@user_app.route('/email', methods=['POST'])
def check_if_email_exist():
    """이메일 중복 확인

        Args:
            email : 사용자의 이메일
    """
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json
        email = model_dao.search_email(db, data['email'])

        if email:
            return jsonify(message = "EMAIL_ALREADY_EXIST"), 400
        return jsonify(message = "AVAILABLE_EMAIL"), 200

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

@user_app.route('/nickname', methods=['POST'])
def check_if_nickname_exist():
    """닉네임 중복 확인

        Args:
            nickname : 사용자의 닉네임
    """
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json
        nickname = model_dao.search_nickname(db, data['nickname'])

        if nickname:
            return jsonify(message = "NICKNAME_ALREADY_EXIST"), 400
        return jsonify(message = "AVAILABLE_NICKNAME"), 200

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

@user_app.route('/sign-in', methods=['POST'])
def sign_in():
    """이메일 로그인

        Args:
            email : 사용자의 이메일
            password : 사용자의 비밀번호

        Returns:
            token : 로그인시 발행되는 JWT 토큰
    """
    db = None
    try:
        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = request.json
        user = model_dao.search_email(db, data['email'])

        if user:
            if bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode(
                    {
                        'id': user['id'],
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    },
                    SECRET_KEY,
                    ALGORITHM
                ).decode('utf-8')
                return jsonify(token = token), 200

            return jsonify(message = "PASSWORD_DOES_NOT_MATCH"), 400
        return jsonify(message = "EMAIL_DOES_NOT_EXIST"), 400

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

#회원 탈퇴
@user_app.route('', methods=['DELETE'])
@login_required
def membership_withdrawal(**kwargs):
    """회원 탈퇴 API

    Headers:
        token

    Args:
        None

    Return:
        None

    Exceptions:
        InternalError: DATABASE가 존재하지 않을 때 발생
        OperationalError: DATABASE 접속이 인가되지 않았을 때 발생
        ProgramingError: SQL syntax가 잘못되었을 때 발생
        IntergrityError: Key의 무결성을 헤쳤을 때 발생
        DataError: 컬럼 타입과 매칭되지 않는 값이 DB에 전달되었을 때 발생
        KeyError: 엔드포인트에서 요구하는 키값이 전달되지 않았을 때 발생
    """
    db = None
    try:
        user_id = kwargs['id']

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        db.begin()
        model_dao.delete_user(db, user_id)
        model_dao.delete_user_diary(db, user_id)
        model_dao.delete_user_series(db, user_id)
        model_dao.delete_user_like(db, user_id)

        db.commit()
        return(''), 200

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
            db.close

#google 로그인
@user_app.route('/google', methods=['POST'])
def google():
    db = None
    try:

        data = request.json

        GOOGLE_AUTH_URL = 'https://oauth2.googleapis.com/tokeninfo?id_token='
        CORRECT_ISS_LIST = ['accounts.google.com', 'https://accounts.google.com']

        google_id = data['googleId']
        google_token = data['token']
        nickname = request.get_json(silent=True).get('nickname', None)

        token_data = json.loads(requests.get(GOOGLE_AUTH_URL + google_token).text)

        if (token_data['iss'] not in CORRECT_ISS_LIST) or (token_data['sub'] != google_id):
            return {'message': 'MODIFIED_TOKEN'}, 401

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        google_user = model_dao.serch_google_user(db, google_id)
        # 가입된 계정인 경우 로그인 진행
        if google_user:
            token = jwt.encode(google_user, SECRET_KEY, ALGORITHM)
            return jsonify(token=token.decode('utf-8'), nickname=nickname), 200

        elif google_user is None:
            db.begin()
            social_id = model_dao.insert_google_user(db, google_id)
            if nickname:
                google_user = model_dao.insert_google_into_user(db, social_id, nickname)
                token = jwt.encode(google_user, SECRET_KEY, ALGORITHM)
                return jsonify(token=token.decode('utf-8'), nickname=nickname), 200

            elif nickname is None:
                return jsonify(message="DATA_ERROR"), 400
            db.commit()

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

#회원정보 보기
@login_required
@user_app.route('/information', methods=['GET'])
def select_member_information(**kwargs):
    db = None
    try:
        user_id = kwargs['id']

        db = db_connector()

        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        data = model_dao.select_user_information(db, user_id)

        return jsonify(data), 200
    except Exception as e:
        return jsonify(message=f"{e}"), 500
    finally:
        if db:
            db.close()

#회원정보 수정
@login_required
@user_app.route('/information', methods=['PUT'])
def modifying_member_information(**kwargs):
    db = None
    try:
        data = request.json
        user_id = kwargs['id']

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        #회원 정보 변경 전 기존 비밀번호 확인
        if bcrypt.checkpw(data['password'].encode('utf-8'), kwargs['password'].encode('utf-8')):

            #닉네임 검사 후 있는 닉네임이면 변경 불가
            nickname = model_dao.search_nickname(db, data['nickname'])
            if nickname:
                return jsonify(message = "NICKNAME_ALREADY_EXiST"), 400

            #비밀번호를 변경 했다면 새 비밀번호와 닉네임 저장 후 새 토큰 발행
            if data['new_password'] != None:
                new_password = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())

                db.begin()
                model_dao.put_user_information(db, data['nickname'], new_password, user_id)
                db.commit()

                #새 토큰 발행
                new_user = model_dao.search_email(db, kwargs['email'])
                token = jwt.encode(
                    {
                        'id': new_user['id'],
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    },
                    SECRET_KEY,
                    ALGORITHM
                ).decode('utf-8')
                return jsonify(token = token), 200

            #닉네임만 변경했을 때
            else:
                db.begin()
                model_dao.put_user_nickname(db, data['nickname'], user_id)
                db.commit()
                return (''), 200

        #기존 비밀번호 틀렸을 때
        return jsonify(message = "PASSWORD_DOES_NOT_MATCH" ), 400

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

@user_app.route('/password', methods=['POST'])
def change_password():
    db = None
    try:
        # 사용자 email 받아옴
        email = request.json['email']

        # random한 임시 비밀번호 생성
        symbols = ascii_letters + digits + punctuation
        secure_random = random.SystemRandom()
        password = "".join(secure_random.choice(symbols) for i in range(10))

        temporary_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = db_connector()
        if db is None:
            return jsonify(message="DATABASE_INIT_ERROR"), 500

        user_email = model_dao.search_email(db, email)
        if user_email is None:
            return jsonify(message="DATA_ERROR"), 400

        db.begin()
        model_dao.update_password(db, temporary_password, email)
        db.commit()

        send_email(password, email)
        return(''), 200

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
            db.close
