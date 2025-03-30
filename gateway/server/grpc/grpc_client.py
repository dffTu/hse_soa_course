import grpc

import server.grpc.posts_pb2_grpc as posts_pb2_grpc
import server.grpc.posts_pb2 as posts_pb2
import server.api.schemas as schemas

class GrpcClient:
    def __init__(self, address: str):
        self.__address = address
        self.__channel = grpc.insecure_channel(self.__address)
        self.__stub = posts_pb2_grpc.PostsServiceStub(self.__channel)
    
    def create_post(self, create_post_request: schemas.CreatePostRequest) -> schemas.CreatePostResponse:
        response = self.__stub.CreatePost(posts_pb2.CreatePostRequest(
            name=create_post_request.name,
            description=create_post_request.description,
            author_id=create_post_request.author_id,
            is_private=create_post_request.is_private,
            tags=create_post_request.tags
        ))
        return schemas.CreatePostResponse(post_id=response.post_id)

    def update_post(self, update_post_request: schemas.UpdatePostRequest) -> schemas.Post:
        pass
    
    def delete_post(self, delete_post_request: schemas.DeletePostRequst) -> schemas.Post:
        pass

    def get_post(self, get_post_request: schemas.GetPostRequest) -> schemas.Post:
        pass

    def get_posts_pages(self, get_post_paged_request: schemas.GetPostsPagedRequest) -> schemas.GetPostsPagedResponse:
        pass
