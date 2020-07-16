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

    def my_series(self, db, user_id):
        """
        user에 따른 모든 series조회
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id, name FROM series
                WHERE user_id = %s
                AND is_deleted = 0
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
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

    def count_series_diary(self, db, user_id, series_id):
        """
        시리즈안에 포함된 다이어리 갯수
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT COUNT(*) FROM diaries
                WHERE user_id = %s AND series_id = %s
                """
                affected_row = cursor.execute(query, (user_id, series_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchone()['COUNT(*)']
        except Exception as e:
            raise e

    def update_series_name(self, db, name, series_id):
        """
        시리즈 이름 변경
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE series SET name = %s
                WHERE id = %s
                """
                affected_row = cursor.execute(query, (name, series_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def delete_series_from_db(self, db, series_id, user_id):
        """
        시리즈 소프트 딜리트
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE series set is_deleted = 1
                WHERE id = %s AND user_id = %s
                """
                affected_row = cursor.execute(query, (series_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def delete_series_from_diaries(self, db, series_id, user_id):
        """
        다이어리에서 해당 시리즈 삭제
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE diaries SET series_id = NULL
                WHERE series_id = %s AND user_id = %s
                """
                affected_row = cursor.execute(query, (series_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def search_diaries_in_series(self, db, series_id, user_id):
        """
        시리즈에 있는 다이어리 조회
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT diaries.id, emotion_id, image_url, color, summary, public, likes.is_deleted FROM diaries
                INNER JOIN emotions ON diaries.emotion_id = emotions.id
                LEFT JOIN likes ON diaries.id = likes.diary_id
                WHERE series_id = %s AND diaries.user_id = %s
                """
                affected_row = cursor.execute(query, (series_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except Exception as e:
            raise e

    def count_likes(self, db, diary_id):
        """
        좋아요 갯수
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT COUNT(*) FROM likes
                WHERE diary_id = %s AND is_deleted = 0
                """
                affected_row = cursor.execute(query, diary_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchone()['COUNT(*)']
        except Exception as e:
            raise e

    def delete_series_from_diaries(self, db, series_id, user_id):
        """
        다이어리에서 해당 시리즈 삭제
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE diaries SET series_id = NULL
                WHERE series_id = %s AND user_id = %s
                """
                affected_row = cursor.execute(query, (series_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def search_emotion(self, db):
        """
        모든 감정 정보 보여주기
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id, name, image_url, color FROM emotions
                """
                affected_row = cursor.execute(query)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except Exception as e:
            raise e

    def update_series(self, db, series_id, diary_id, user_id):
        """
        시리즈에 다이어리 추가
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE diaries SET series_id = %s
                WHERE id IN %s AND user_id = %s AND is_deleted = 0
                """
                affected_row = cursor.execute(query, (series_id, diary_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e
