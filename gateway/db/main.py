import psycopg2
import db.config as config

class Database:
    def __init__(self):
        self.__db = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
    
    def add_something(self):
        cur = self.__db.cursor()
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        cur.close()
