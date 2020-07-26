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
            with db.cursor() as cursor:
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
            with db.cursor() as cursor:
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
                WHERE diaries.is_deleted = 0 AND public = 1 AND is_completed = 1
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

    def pagination(self, filter_dict):
        """
        페이지네이션 함수
        """
        try:
            pagination_query = "LIMIT %(limit)s "
            if filter_dict['offset']:
                query = "OFFSET %(offset)s "
                pagination_query = pagination_query + query

            return pagination_query

        except Exception as e:
            raise e

    def search_all_diaries(self, db, filter_dict):
        """
        모든 다이어리 모아 보기
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query ="""
                SELECT diaries.id, emotion_id, image_url, color, summary, public, is_completed, diaries.created_at, diaries.is_deleted, likes.is_deleted, users.nickname FROM diaries
                INNER JOIN emotions ON diaries.emotion_id = emotions.id
                INNER JOIN users ON diaries.user_id = users.id
                LEFT JOIN likes ON diaries.id = likes.diary_id
                WHERE diaries.is_deleted = 0 AND public = 1 AND is_completed = 1
                """
                order_by_query ="""
                ORDER BY diaries.created_at DESC
                """

                pagination_query = self.pagination(filter_dict)
                filter_query = self.diary_filter(filter_dict)

                query = query + filter_query + order_by_query + pagination_query

                print(query)
                affected_row = cursor.execute(query, filter_dict)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except  Exception as e:
            raise e

    def search_is_like(self, db, user_id, diary_id):
        """
        해당 유저가 해당 다이어리에 좋아요 눌렀는지 확인
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT COUNT(*) FROM whisper.likes
                WHERE user_id = %s AND diary_id = %s AND is_deleted = 0
                """
                affected_row = cursor.execute(query, (user_id, diary_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()['COUNT(*)']
        except Exception as e:
            raise e

    def insert_google_into_user(self, db, social_id, nickname):
        """google 회원가입 user를 user에 추가.

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

    def insert_google_user(self, db, kakao_id):
        """google 회원가입.

        Args:
            kakao_id: 카카오톡 소셜 아이디

        Return:
           socials 테이블의 마지막 column의 id
        """
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO socials(google_id, type)
                VALUES(%s,'google')
                """
                affected_row = cursor.execute(query, google_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')
                return cursor.lastrowid
        except Exception as e:
            raise e

    def search_google_user(self, db, google_id):
        """google 소셜 로그인.

        Args:
        google_id: 구글 소셜 아이디

        Return:
        google_id가 있으면 user_id 없으면 None

        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query ="""
                SELECT users.id FROM users INNER JOIN socials
                ON users.social_id = socials.id
                WHERE google_id = %s
                """
                affected_row = cursor.execute(query, google_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')
                elif affected_row == 1:
                    return cursor.fetchone()
                elif affected_row == 0:
                    return None
        except Exception as e:
            raise e

    def diary_filter(self, filter_dict):
        """다이어리 필터용 함수
        """
        try:
            filter_query = ""
            queries = ""
            if filter_dict['emotion']:
                for i in range(0, len(filter_dict['emotion'])):
                    emotion = int(filter_dict['emotion'][i])
                    if i == 0:
                        query = f"AND (emotion_id = {emotion} "
                    else:
                        query = f"OR emotion_id = {emotion} "
                    queries += query
                filter_query += f"{queries})"

            if filter_dict['startdate']:
                query = "AND diaries.created_at >= %(startdate)s "
                filter_query += query

            if filter_dict['enddate']:
                query = "AND diaries.created_at <= %(enddate)s "
                filter_query += query

            if filter_dict['filter']:
                if filter_dict['filter'] == 'like':
                    query = "AND likes.user_id = %(user_id)s "
                    filter_query += query
                if filter_dict['filter'] == 'popular':
                    query = ""

            return filter_query
        except  Exception as e:
            raise e

    def diary_like_filter(self, db):
        """다이어리 좋아요 수 order_by
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT diary_id, COUNT(user_id) AS cnt
                FROM likes
                WHERE is_deleted=0
                GROUP BY diary_id
                ORDER BY cnt DESC
                """
                affected_row = cursor.execute(query)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchall()
        except Exception as e:
            raise e

    def select_user_information(self, db, user_id):
        """
        유저 정보 조회
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                SELECT email, nickname FROM users
                WHERE id = %s
                """
                affected_row = cursor.execute(query, user_id)
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return cursor.fetchone()
        except Exception as e:
            raise e

    def put_user_information(self, db, user_nickname, user_password, user_id):
        """
        유저 비밀번호와 닉네임 변경
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE users SET nickname = %s, password = %s
                WHERE id = %s
                """
                affected_row = cursor.execute(query, (user_nickname, user_password, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e

    def put_user_nickname(self, db, user_nickname, user_id):
        """
        유저 닉네임 변경
        """
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                UPDATE users SET nickname = %s
                WHERE id = %s
                """
                affected_row = cursor.execute(query, (user_nickname, user_id))
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except  Exception as e:
            raise e

    def insert_diary(self, db, user_id, emotion_id, contents, summary, is_completed, public, series_id):
        """
        새 다이어리 생성
        """
        try:
            with db.cursor() as cursor:
                query = """
                    INSERT INTO diaries(
                        user_id,
                        emotion_id,
                        contents,
                        summary,
                        is_completed,
                        public,
                        series_id
                        )
                    VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        )
                    """
                affected_row = cursor.execute(query, (user_id, emotion_id, contents, summary, is_completed, public, series_id))
                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                elif affected_row == 1:
                    return cusor.fetchone()
        except Exception as e:
            raise e

    def select_diary(self, db, user_id, diary_id):
        """작성한 다이어리 가져오기"""
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    SELECT emotion_id, series_id, contents, summary, is_compelted, public FROM diaries
                    WHERE user_id = %s AND diary_id = %s
                    """
                affected_row = cursor.execute(query, (user_id, diary_id))

                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()

        except Exception as e:
            raise e

    def update_diary(self, db, user_id, emotion_id, contents, summary, is_completed, is_public, series_id):
        """다이어리 수정"""
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    UPDATE diaries
                    SET emotion_id = %s, series_id = %s, contents = %s, summary = %s, is_completed = %s, public = %s
                    WHERE user_id = %s AND diary_id = %s
                    """
                affected_row = cursor.execute(query, (emotion_id, series_id, contents, summary, is_completed, is_public, user_id, diary_id))

                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()

        except Exception as e:
            raise e

    def delete_diary(self, db, user_id, diary_id):
        """다이어리 삭제하기"""
        try:
            with db.cursor() as cursor:
                query = """
                    UPDATE diaries
                    SET is_deleted = 1
                    WHERE user_id = %s AND diary_id = %s
                    """
                affected_row = cursor.execute(query, (user_id, diary_id))
                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()

        except Exception as e:
            raise e

    def delete_liked_diary(self, db, user_id, diary_id):
        """다이어리 좋아요 취소"""
        try:
            with db.cursor() as cursor:
                query = """
                    UPDATE diaries
                    SET is_deleted = 1
                    WHERE user_id = %s AND diary_id = %s
                    """
                affected_row = cursor.execute(query, (user_id, diary_id))
                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()
        except Exception as e:
            raise e

    def like_diary(self, db, user_id, diary_id):
        """다이어리 좋아요"""
        try:
            with db.cursor() as cursor:
                query = """
                    INSERT INTO likes(user_id, diary_id)
                    VALUES(%s, %s)
                    """
                affected_row = cursor.execute(query, (user_id, diary_id))

                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()

        except Exception as e:
            raise e
   
    def get_this_week_diaries(self, db, user_id):
        """이번주에 작성한 다이어리 가져오기"""
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """
                    SELECT diaries.id, weekday(created_at), emotion_id, emotions.image_url, emotions.color, summary FROM diaries
                    INNER JOIN emotions ON diaries.emotion_id = emotions.id 
                    WHERE diaries.user_id = %s and is_completed = 1 AND created_at BETWEEN ADDDATE( CURDATE(), - WEEKDAY(CURDATE()) + 0 ) AND ADDDATE( CURDATE(), - WEEKDAY(CURDATE()) + 6 )
                    """
                affected_row = cursor.execute(query, user_id)

                if affected_row == -1:
                    raise Exception("EXECUTED_FAILED")
                return cursor.fetchone()

        except Exception as e:
            raise e
