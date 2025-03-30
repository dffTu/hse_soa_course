import psycopg2
import json
import os
from typing import Optional
from datetime import datetime

class Database:
    def __init__(self):
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
        self.__cursor = self.__conn.cursor()
    
    def create_post(self, name: str, description: str, author_id: int, tags: dict, is_private: Optional[bool] = None) -> int:
        creation_timestamp = datetime.now()

        if is_private is not None:
            self.__cursor.execute('INSERT INTO posts (name, description, author_id, created_at, updated_at, is_private, tags) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                        (name, description, author_id, creation_timestamp, creation_timestamp, is_private, json.dumps(tags)))
        else:
            self.__cursor.execute('INSERT INTO posts (name, description, author_id, created_at, updated_at, tags) '
                        'VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                        (name, description, author_id, creation_timestamp, creation_timestamp, json.dumps(tags)))
        post_id = self.__cursor.fetchone()[0]

        return post_id
