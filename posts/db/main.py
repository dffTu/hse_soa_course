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
    
    def create_post(self, name: str, description: str, author_id: int, tags: dict, is_private: bool) -> int:
        creation_timestamp = datetime.now()

        self.__cursor.execute('INSERT INTO posts (name, description, author_id, created_at, updated_at, tags) '
                              'VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                              (name, description, author_id, creation_timestamp, creation_timestamp, json.dumps(tags)))
        post_id = self.__cursor.fetchone()[0]
        self.__conn.commit()

        return post_id
    
    def update_post(self, post_id: int, name: str, description: str, tags: dict, is_private: bool) -> dict | None:
        self.__cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id, ))
        if self.__cursor.fetchone() is None:
            return None
        
        self.__cursor.execute('UPDATE posts SET name = %s, description = %s, updated_at = %s, tags = %s, is_private = %s '
                              'WHERE id = %s RETURNING name, description, author_id, is_private, tags, created_at, updated_at',
                              (name, description, datetime.now(), json.dumps(tags), is_private, post_id))
        name, description, author_id, is_private, tags, created_at, updated_at = self.__cursor.fetchone()
        tags = json.loads(tags)
        result = {
            'name': name,
            'description': description,
            'author_id': author_id,
            'is_private': is_private,
            'tags': tags,
            'created_at': created_at,
            'updated_at': updated_at
        }
        self.__conn.commit()

        return result
    
    def delete_post(self, post_id: int) -> dict | None:
        self.__cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id, ))
        if self.__cursor.fetchone() is None:
            return None
        
        self.__cursor.execute('DELETE FROM posts WHERE id = %s RETURNING name, description, author_id, is_private, tags, created_at, updated_at',
                              (post_id, ))
        name, description, author_id, is_private, tags, created_at, updated_at = self.__cursor.fetchone()
        tags = json.loads(tags)
        result = {
            'name': name,
            'description': description,
            'author_id': author_id,
            'is_private': is_private,
            'tags': tags,
            'created_at': created_at,
            'updated_at': updated_at
        }
        self.__conn.commit()

        return result
    
    def get_post(self, post_id: int) -> dict | None:
        self.__cursor.execute('SELECT name, description, author_id, is_private, tags, created_at, updated_at FROM posts WHERE id = %s', (post_id, ))
        result = self.__cursor.fetchone()
        if result is None:
            return None
        
        name, description, author_id, is_private, tags, created_at, updated_at = result
        tags = json.loads(tags)
        result = {
            'name': name,
            'description': description,
            'author_id': author_id,
            'is_private': is_private,
            'tags': tags,
            'created_at': created_at,
            'updated_at': updated_at
        }

        return result
    
    def get_posts_paged(self, page: int, page_size: int) -> dict:
        self.__cursor.execute('SELECT COUNT(*) FROM posts')
        total_posts = self.__cursor.fetchone()[0]

        self.__cursor.execute('SELECT name, description, author_id, is_private, tags, created_at, updated_at FROM posts LIMIT %s OFFSET %s',
                              (page_size, (page - 1) * page_size))
        posts = self.__cursor.fetchall()

        posts = [
            {
                'name': name,
                'description': description,
                'author_id': author_id,
                'is_private': is_private,
                'tags': json.loads(tags),
                'created_at': created_at,
                'updated_at': updated_at
            } for name, description, author_id, is_private, tags, created_at, updated_at in posts
        ]
        
        result = {
            'total_posts': total_posts,
            'posts': posts,
            'page': page,
            'total_pages': (total_posts + page_size - 1) // page_size
        }

        return result
