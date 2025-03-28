import random
import string
import psycopg2
import time
import os
from typing import Optional, Union
from datetime import datetime, timezone

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
        creation_timestamp = datetime.now(timezone.utc)
        
        cursor.execute('INSERT INTO accounts (creation_timestamp) VALUES (%s) RETURNING id',
                       (creation_timestamp, ))
        account_id = cursor.fetchone()[0]

        cursor.execute('INSERT INTO logins (account_id, login, hashed_password, is_freezed, login_tries_in_1h) VALUES (%s, %s, %s, FALSE, 0)',
                       (account_id, login, hashed_password))
        
        cursor.execute('INSERT INTO user_info (account_id, email) VALUES (%s, %s)',
                       (account_id, email))
        
        self.__conn.commit()

        return True
    
    def auth_user(self, login: str, password: str) -> Union[None, str]:
        cursor = self.__conn.cursor()
        hashed_password = str(hash(password))

        cursor.execute(f'SELECT * FROM logins WHERE login = %s AND hashed_password = %s',
                       (login, hashed_password))
        logins = cursor.fetchall()
        if len(logins) == 0:
            return None
        
        account_id = logins[0][0]
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        cursor.execute('INSERT INTO tokens (account_id, token) VALUES (%s, %s)',
                       (account_id, token))
        
        last_login_timestamp = datetime.now(timezone.utc)
        cursor.execute('UPDATE user_info SET last_login = %s WHERE account_id = %s',
                       (last_login_timestamp, account_id))
        
        self.__conn.commit()

        return token

    def change_user_info(
            self,
            token: str,
            name: Optional[str],
            surname: Optional[str],
            birthday: Optional[str],
            email: Optional[str],
            phone_number: Optional[str],
            city: Optional[str]
        ) -> bool:
        cursor = self.__conn.cursor()

        cursor.execute(f'SELECT * FROM tokens WHERE token = %s',
                       (token, ))
        account_id = cursor.fetchone()
        if account_id is None:
            return False
        account_id = account_id[0]

        if name is not None:
            cursor.execute('UPDATE accounts SET name = %s WHERE id = %s', 
                           (name, account_id))
        if surname is not None:
            cursor.execute('UPDATE accounts SET surname = %s WHERE id = %s', 
                           (surname, account_id))
        if birthday is not None:
            cursor.execute('UPDATE user_info SET birthday = %s WHERE account_id = %s', 
                           (birthday, account_id))
        if email is not None:
            cursor.execute('UPDATE user_info SET email = %s WHERE account_id = %s', 
                           (email, account_id))
        if phone_number is not None:
            cursor.execute('UPDATE user_info SET phone_number = %s WHERE account_id = %s', 
                           (phone_number, account_id))
        if city is not None:
            cursor.execute('UPDATE user_info SET city = %s WHERE account_id = %s', 
                           (city, account_id))

        last_update_timestamp = datetime.now(timezone.utc)
        cursor.execute('UPDATE user_info SET last_update_info = %s WHERE account_id = %s',
                       (last_update_timestamp, account_id))
        
        self.__conn.commit()

        return True

users_db = Database()
