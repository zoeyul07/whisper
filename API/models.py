import pymysql

class ModelDao:
    def insert_series(self, db, user_id, name):
        """
        시리즈 생성
        """
        try:
            with db.cursor() as cursor:
                query = """
                INSERT INTO serires(user_id, name)
                VALIES(%s, %s)
                """
                affected_row = cursor.execute(query, (user_id, name))
                # execute 에러 처리
                if affected_row == -1:
                    raise Exception('EXECUTE_FAILED')

                return None
        except Exception as e:
            raise e
