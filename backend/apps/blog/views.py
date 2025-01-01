from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime

from apps.blog.serializers import PostInputSerializer, PostOutputSerializer
from apps.blog.pagination import PostPagination
from apps.blog.models import Post


def generate_response(status_code, message, data=None):
    """
    Helper function to generate consistent API responses.

    Args:
        status_code (int): HTTP status code for the response.
        message (str): Message explaining the response.
        data (dict, optional): Data to be included in the response. Defaults to None.

    Returns:
        Response: The formatted response with status, message, timestamp, and data.
    """
    return Response({
        'status_code': status_code,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'data': data or {}
    })


class PostListCreateView(generics.ListCreateAPIView):
    """
    View for listing posts and creating a new post.
    """
    queryset = Post.objects.all()
    pagination_class = PostPagination

    def get_serializer_class(self):
        """Choose serializer dynamically based on request method."""
        if self.request.method == 'GET':
            return PostOutputSerializer
        return PostInputSerializer

    def perform_create(self, serializer):
        """Override to handle creation logic."""
        serializer.save()

    def post(self, request, *args, **kwargs):
        """
        Handle the creation of a new post.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return generate_response(status.HTTP_201_CREATED, "Post has been created successfully", serializer.data)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting posts.
    """
    queryset = Post.objects.all()

    def get_serializer_class(self):
        """Choose serializer dynamically based on request method."""
        if self.request.method == 'GET':
            return PostOutputSerializer
        return PostInputSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Handle the retrieval of a single post.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return generate_response(status.HTTP_200_OK, "Post retrieved successfully", serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Handle the update of an existing post.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return generate_response(status.HTTP_200_OK, "Post has been updated successfully", serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of a post.
        """
        instance = self.get_object()
        instance.delete()
        return generate_response(status.HTTP_204_NO_CONTENT, "Post has been deleted successfully", None)
