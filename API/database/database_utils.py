import os, sys

BASE_DIR = os.path.dirname(os.path.abspath("API"))
sys.path.extend([BASE_DIR])

from my_settings import MYSQL_CONFIGS

DB_NAME = MYSQL_CONFIGS['database']


def init_databases(db):
    cursor = db.cursor()
    db.begin()
    cursor.execute("DROP DATABASE " + DB_NAME)
    cursor.execute("CREATE DATABASE " + DB_NAME + " character set utf8mb4 collate utf8mb4_general_ci")
    cursor.execute("use " + DB_NAME)
    db.commit()
    cursor.close()

def import_aquery(file):
    file.readline()
    aquery = file.read()
    aquery = aquery.replace("-- users Table Create SQL", " ")
    aquery = aquery.replace("\n", " ")
    aquery = " ".join(aquery.split())
    aquery = aquery.replace("`created_at`  DATETIME", "`created_at`  DATETIME DEFAULT CURRENT_TIMESTAMP ")

    return aquery.split(';')[:-1]
