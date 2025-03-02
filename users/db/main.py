import psycopg2
import time
import os

class Database:
    def __init__(self):
        time.sleep(5)
        self.__conn = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )

        scripts_directory = os.fsencode("db/scripts")
    
        for script in os.listdir(scripts_directory):
            filename = os.fsdecode(script)
            self.__conn.cursor().execute(open("db/scripts/" + filename, "r").read())
        self.__conn.commit()

users_db = Database()
