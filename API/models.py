import pymysql

class ModelDao:
    def insert_series(self, db, user_id, name):
        """
        시리즈 생성
        """
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO series(user_id, name)
                VALUES(%s, %s)
                """
                affected_row = cursor.execute(query, (user_id, name))
                # execute 에러 처리
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def search_series(self, db, user_id, name):
        """
        시리즈 조회
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id FROM series
                WHERE user_id = %s AND name = %s
                """
                affected_row = cursor.execute(query, (user_id, name))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')
                elif affected_row == 0:
                    return None
                return cursor.fetchone()['id']

        except Exception as e:
            raise e

    def search_kakao_user(self, db, kakao_id):
        """
        kakao 로그인
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query ="""
                SELECT users.id FROM users INNER JOIN socials
                ON users.social_id = socials.id
                WHERE kakao_id = %s;
                """
                affected_row = cursor.execute(query, kakao_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')
                elif affected_row == 1:
                    return cursor.fetchone()
                elif affected_row == 0:
                    return None

        except Exception as e:
            raise e

    def insert_kakao_user(self, db, kakao_id):
        """
        kakao 회원가입
        """
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO socials(kakao_id, type)
                VALUES(%s,'kakao')
                """
                affected_row = cursor.execute(query, kakao_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.lastrowid
        except Exception as e:
            raise e

    def insert_kakao_into_user(self, db, social_id, nickname):
        """
        kakao 회원가입
        """
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO users(social_id, nickname)
                VALUES(%s, %s)
                """
                affected_row = cursor.execute(query, (social_id, nickname))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.lastrowid
        except Exception as e:
            raise e
