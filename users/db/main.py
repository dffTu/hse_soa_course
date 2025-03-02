import psycopg2
import time
import os

class Database:
    def __init__(self):
        time.sleep(5)
        self.__db = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )
    
    def add_something(self):
        cur = self.__db.cursor()
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        self.__db.commit()
        cur.close()
