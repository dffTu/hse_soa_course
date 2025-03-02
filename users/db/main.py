import psycopg2
import time
import os
import sys

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
        scripts = [os.fsdecode(script) for script in os.listdir(scripts_directory)]
    
        for script in sorted(scripts):
            self.__conn.cursor().execute(open("db/scripts/" + script, "r").read())
        self.__conn.commit()
    
    def register_user(self, login: str, email: str, password: str) -> bool:
        cursor = self.__conn.cursor()
        cursor.execute(f'SELECT * FROM logins WHERE login = \'{login}\'')
        found_logins = cursor.fetchall()
        if len(found_logins) > 0:
            return False

        hashed_password = str(hash(password))
        
        cursor.execute('INSERT INTO accounts DEFAULT VALUES RETURNING id')
        account_id = cursor.fetchone()[0]

        cursor.execute('INSERT INTO logins (account_id, login, hashed_password, is_freezed, login_tries_in_1h) ' \
                       f'VALUES ({account_id}, \'{login}\', \'{hashed_password}\', FALSE, 0)')
        
        cursor.execute('INSERT INTO user_info (account_id, email) ' \
                       f'VALUES ({account_id}, \'{email}\')')
        
        self.__conn.commit()

        return True

users_db = Database()
