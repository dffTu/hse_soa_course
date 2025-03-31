from concurrent import futures
import grpc
import server.grpc.posts_pb2 as posts_pb2
import server.grpc.posts_pb2_grpc as posts_pb2_grpc
import logging

import server.config as config
from db.main import Database

class Service(posts_pb2_grpc.PostsServiceServicer):
    def __init__(self):
        super().__init__()
        self.__db = Database()
        self.__logger = logging.getLogger(__name__)

    def CreatePost(self, request, context):
        tags = [str(tag) for tag in request.tags]
        post_id = self.__db.create_post(
            name=request.name,
            description=request.description,
            author_id=request.author_id,
            is_private=request.is_private,
            tags=dict({'tags': tags})
        )
        return posts_pb2.CreatePostResponse(post_id=post_id)

    def UpdatePost(self, request, context):
        tags = [str(tag) for tag in request.tags]
        data = self.__db.update_post(
            post_id=request.post_id,
            name=request.name,
            description=request.description,
            is_private=request.is_private,
            tags=dict({'tags': tags})
        )
        if data is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post with such id doesn't exist!")
        return posts_pb2.Post(
            name=data['name'],
            description=data['description'],
            author_id=data['author_id'],
            is_private=data['is_private'],
            tags=data['tags'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

    def DeletePost(self, request, context):
        data = self.__db.delete_post(
            post_id=request.post_id
        )
        if data is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post with such id doesn't exist!")
        return posts_pb2.Post(
            name=data['name'],
            description=data['description'],
            author_id=data['author_id'],
            is_private=data['is_private'],
            tags=data['tags'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

    def GetPost(self, request, context):
        data = self.__db.get_post(
            post_id=request.post_id
        )
        if data is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post with such id doesn't exist!")
        return posts_pb2.Post(
            name=data['name'],
            description=data['description'],
            author_id=data['author_id'],
            is_private=data['is_private'],
            tags=data['tags'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

    def GetPostsPaged(self, request, context):
        data = self.__db.get_posts_paged(
            page=request.page,
            page_size=request.page_size
        )
        
        posts = [
            posts_pb2.Post(
                name=post['name'],
                description=post['description'],
                author_id=post['author_id'],
                is_private=post['is_private'],
                tags=post['tags'],
                created_at=post['created_at'],
                updated_at=post['updated_at']
            ) for post in data['posts']
        ]

        return posts_pb2.GetPostsPagedResponse(
            posts=posts,
            page=data['page'],
            total_pages=data['total_pages'],
            total_posts=data['total_posts']
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostsServiceServicer_to_server(
        Service(), server)
    server.add_insecure_port(f'{config.SERVER_IP}:{config.PORT}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()