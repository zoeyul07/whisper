import pymysql

from my_settings import MYSQL_CONFIGS

def db_connector():
    connector = pymysql.connect(**MYSQL_CONFIGS)
    return connector
