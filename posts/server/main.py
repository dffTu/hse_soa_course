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
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPostsPaged(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostsServiceServicer_to_server(
        Service(), server)
    server.add_insecure_port(f'{config.SERVER_IP}:{config.PORT}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()