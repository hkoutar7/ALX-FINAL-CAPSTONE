from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse


from config.response import generate_response
from apps.blog.serializers import PostCreateSerializer, PostViewSerializer
from apps.blog.pagination import PostPagination
from apps.blog.models import Post



class PostListCreateView(APIView):
    """
        View for listing posts and creating a new post.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        summary="Retrieve a list of posts",
        description="Get a list of all posts.",
        responses={
            200: OpenApiResponse(description='List of posts', response=PostViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def get(self, request):
        try:
            posts = Post.objects.all()
            serializer = PostViewSerializer(posts, many=True)
            return generate_response(status.HTTP_200_OK, "Posts retrieved successfully", serializer.data)
        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred while retrieving posts.", str(e))


    @extend_schema(
        tags=["Post"],
        summary="Create a new post",
        request=PostCreateSerializer,
        description="Create a new blog post.",
        responses={
            201: OpenApiResponse(description='Post created successfully', response=PostViewSerializer),
            400: OpenApiResponse(description='Validation error'),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def post(self, request):
        try:
            serializer = PostCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user)
            return generate_response(status.HTTP_201_CREATED, "Post created successfully", serializer.data)
        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred while creating the post.", str(e))






