import pymysql

class ModelDao:
    def insert_series(self, db, user_id, name):
        """시리즈 생성.

        Args:
            user_id: 사용자 id
            name: 시리즈 명

        Return:
            None
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
        """시리즈 조회.

        Args:
            user_id: 사용자 id
            name: 시리즈 이름

        Return:
            해당 시리즈의 id
            시리즈가 없으면 None
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
        """해당user의 모든 series조회.

        Args:
            user_id: 사용자 id

        Return:
            user가 가지고있는 모든 series의 id, name
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
        """kakao 소셜 로그인.

        Args:
            kakao_id: 카카오톡 소셜 아이디

        Return:
            kakao_id가 있으면 user_id
            없으면 None
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query ="""
                SELECT users.id, users.nickname FROM users INNER JOIN socials
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
        """kakao 회원가입.

        Args:
            kakao_id: 카카오톡 소셜 아이디

        Return:
           socials 테이블의 마지막 column의 id
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
        """kakao 회원가입 user를 user에 추가.

        Args:
            social_id: 소셜 유저의 id

        Return:
            users 테이블의 마지막 column id
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
        """시리즈안에 포함된 다이어리 갯수.

        Args:
            user_id: 사용자 id
            series_id: 시리즈 id

        Return:
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
        """시리즈 이름 변경.

        Args:
            name: 시리즈 이름
            series_id: 시리즈 id

        Return:
            None
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
        """시리즈 삭제.

        Args:
            series_id: 시리즈 id
            user_id: 사용자 id

        Return:
            None
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
        """다이어리한개에서 해당 시리즈 삭제.

        Args:
            series_id: 시리즈 id
            user_id: 사용자 id

        Return:
            None
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
        """시리즈에 있는 다이어리 조회.

        Args:
            series_id: 시리즈 id
            user_id: 사용자 id

        Return:
            시리즈에 있는 diary들의 정보
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
        """좋아요 갯수.

        Args:
            diary_id: 다이어리 id

        Return:
            해당 다이어리의 좋아요 갯수
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
        """시리즈에 다이어리 추가.

        Args:
            series_id: 시리즈 id
            diary_id: 다이어리 id
            user_id: 사용자 id

        Return:
            None
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

    def search_question(self, db):
        """
        모든 질문 보여주기
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id, contents FROM questions
                """
                affected_row = cursor.execute(query)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except Exception as e:
            raise e

    def delete_diaries_from_series(self, db, diary_id, user_id, series_id):
        """시리즈에서 해당 다이어리들 삭제.

        Args:
            diary_id: 다이어리 id
            user_id: 사용자 id
            series_id: 시리즈 id

        Return:
            None
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE diaries SET series_id = NULL
                WHERE id in %s AND user_id = %s
                AND series_id = %s AND is_deleted = 0
                """
                affected_row = cursor.execute(query, (diary_id, user_id, series_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def create_user(self, db, email, password, nickname):
        """회원가입시 user 생성"""
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO users(email, password, nickname)
                VALUES(%s, %s, %s)
                """
                affected_row = cursor.execute(query, (email, password, nickname))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None

        except Exception as e:
            raise e

    def search_email(self, db, email):
        """가입된 이메일 확인"""
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id, password FROM users
                WHERE email = %s
                """
                affected_row = cursor.execute(query, email)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                elif affected_row == 1:
                    return cursor.fetchone()

                return None

        except Exception as e:
            raise e

    def search_nickname(self, db, nickname):
        """닉네임 중복 확인"""
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT id FROM users
                WHERE nickname = %s
                """
                affected_row = cursor.excute(query, nickname)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                elif affected_row == 1:
                    return cursor.fetchone()

                return None

        except Exception as e:
            raise e

    def change_diary_public(self, db, public, diary_id, user_id):
        """다이어리 공개 여부 변경.

        Args:
            public: 공개 여부
            diary_id: 다이어리 id
            user_id: 사용자 id

        Return:
            None
        """
        try:
            with db.cursor() as cursor:
                query = """
                UPDATE diaries SET public = %s
                WHERE id in %s AND user_id = %s
                AND is_deleted = 0
                """
                affected_row = cursor.execute(query, (public, diary_id, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None

        except Exception as e:
            raise e

    def other_person_diary(self, db, user_id):
        """
        다른 사람 다이어리 모아 보기
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT diaries.id, emotion_id, image_url, color, summary, public, diaries.is_deleted, likes.is_deleted, users.nickname FROM diaries
                INNER JOIN emotions ON diaries.emotion_id = emotions.id
                INNER JOIN users ON diaries.user_id = %s
                LEFT JOIN likes ON diaries.id = likes.diary_id
                WHERE diaries.is_deleted = 0 AND public = 0
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except Exception as e:
            raise e

    def delete_user(self, db, user_id):
        """
        회원 탈퇴
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE users SET is_deleted=1 WHERE id = %s
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def delete_user_diary(self, db, user_id):
        """
        회원탈퇴한 사람 다이어리 일괄 삭제
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE diaries SET is_deleted=1 WHERE user_id = %s
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def delete_user_like(self, db, user_id):
        """
        회원탈퇴한 사람 좋아요 일괄 삭제
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE likes SET is_deleted=1 WHERE user_id = %s
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def delete_user_series(serlf, db, user_id):
        """
        회원탈퇴한 사람 시리즈 일괄 삭제
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE series SET is_deleted=1 WHERE user_id = %s
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def search_all_diaries(self, db):
        """
        모든 다이어리 모아 보기
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query ="""
                SELECT nickname,diaries.id,emotions.id,image_url,color,summary
                """
                affected_row = cursor.execute(query)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except  Exception as e:
            raise e


















