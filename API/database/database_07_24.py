import os, sys
import pymysql

ROOT_DIR = os.path.dirname(os.path.abspath("API"))
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
sys.path.extend([ROOT_DIR])
os.chdir(BASE_DIR)

from database_utils import init_databases, import_aquery
from connections import db_connector

db = db_connector()
cursor = db.cursor()

db.begin()
init_databases(db)

with open('whisper_20200724_33_38.txt', 'r') as f:
    TABLE_QUERIES = import_aquery(f)

for query in TABLE_QUERIES:
    cursor.execute(query)

db.commit()
cursor.close()
db.close()
print('COMPLETE')
