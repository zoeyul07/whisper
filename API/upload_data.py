import csv

from connections import db_connector

csv_list = ['emotions', 'questions']

db = db_connector()
db.begin()
cursor = db.cursor()

for table_name in csv_list:
    path = 'csv/' + table_name + '.csv'
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        records = [x for x in reader]
        columns = records.pop(0)
        values = ('%s,' * len(columns))[:-1]

        query = f"""INSERT INTO {table_name}({','.join(columns)}) VALUES({values})"""
        cursor.executemany(query, records)

db.commit()
cursor.close()
db.close()
print("UPLOAD COMPLETE")
