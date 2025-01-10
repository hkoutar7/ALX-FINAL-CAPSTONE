from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Prefetch
from rest_framework import status
from django.db.models import Q

from config.response import generate_response
from apps.blog.serializers import PostViewSerializer, PostCreateSerializer, PostUpdateSerializer
from apps.blog.models import Post, PostCategory
from apps.blog.pagination import PostPagination 


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
            posts = Post.objects.prefetch_related(
                Prefetch('categories',queryset=PostCategory.objects.select_related('category') ),
                'tags',
                'author'
            )

            serializer = PostViewSerializer(posts, many=True)
            return generate_response(status.HTTP_200_OK, "Posts retrieved successfully", serializer.data)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred while retrieving posts, error: {str(e)}", None)


    @extend_schema(
        tags=["Post"],
        summary="Create a new post",
        description="Create a new post.",
        request=PostCreateSerializer,
        responses={
            201: OpenApiResponse(description='Post created successfully', response=PostViewSerializer),
            400: OpenApiResponse(description='Invalid data'),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = serializer.save(author=request.user)
            response_serializer = PostViewSerializer(post)
            return generate_response(status.HTTP_201_CREATED, "Post created successfully", response_serializer.data)
        except Exception as e:
            return generate_response(status.HTTP_400_BAD_REQUEST, f"Error creating post: {str(e)}", None)



class PostListPaginationView(APIView):
    """
        View for listing posts with pagination.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        parameters=[
            OpenApiParameter(name='page', type=int, description='The page number to retrieve (default is 1)', required=False),
            OpenApiParameter(name='page_size', type=int, description='The number of posts per page (default is 50)', required=False),
        ],
        summary="Retrieve a list of posts with pagination",
        description="Get a list of all posts with pagination support (page, page_size).",
        responses={
            200: OpenApiResponse(description='List of posts', response=PostViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def get(self, request):
        try:
            posts = Post.objects.prefetch_related(
                Prefetch('categories', queryset=PostCategory.objects.select_related('category')),
                'tags',
                'author'
            )

            paginator = PostPagination()
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostViewSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred while retrieving posts, error: {str(e)}", None)



class PostByCategoryView(APIView):
    """
        Retrieve a list of posts filtered by Category.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        summary="Retrieve posts by Category",
        description="Get a list of posts filtered by Category.",
        responses={
            200: OpenApiResponse(description='List of posts by category', response=PostViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        },
        parameters=[
            OpenApiParameter(name='page', type=int, description="Page number for pagination"),
            OpenApiParameter(name='page_size', type=int, description="Number of posts per page"),
        ]
    )
    def get(self, request, category_id):
        try:
            posts = Post.objects.filter(categories__category_id=category_id).prefetch_related(
                'tags',
                'author'
            )

            paginator = PostPagination()
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostViewSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred: {str(e)}", None)



class PostByAuthorView(APIView):
    """
        Retrieve a list of posts written by a specific Author.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        summary="Retrieve posts by Author",
        description="Get a list of posts written by a specific Author.",
        responses={
            200: OpenApiResponse(description='List of posts by author', response=PostViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        },
        parameters=[
            OpenApiParameter(name='page', type=int, description="Page number for pagination"),
            OpenApiParameter(name='page_size', type=int, description="Number of posts per page"),
        ]
    )
    def get(self, request, author_id):
        try:
            posts = Post.objects.filter(author_id=author_id).prefetch_related(
                'tags',
                'categories'
            )

            paginator = PostPagination()
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostViewSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred: {str(e)}", None)



class PostSearchView(APIView):
    """
        Search and filter posts by Title, Content, Tags, or Author.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        summary="Search and filter posts",
        description="Search posts by Title, Content, Tags, or Author.",
        responses={
            200: OpenApiResponse(description='List of filtered posts', response=PostViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        },
        parameters=[
            OpenApiParameter(name='search', type=str, description="Search term for Title, Content, Tags, or Author"),
            OpenApiParameter(name='page', type=int, description="Page number for pagination"),
            OpenApiParameter(name='page_size', type=int, description="Number of posts per page"),
        ]
    )
    def get(self, request):
        search_term = request.query_params.get('search', '')
        posts = Post.objects.all()

        if search_term:
            search_term = search_term.strip()
            posts = posts.filter(
                Q(title__icontains=search_term) | 
                Q(content__icontains=search_term) | 
                Q(tags__name__icontains=search_term) | 
                Q(author__first_name__icontains=search_term) |
                Q(author__last_name__icontains=search_term)
            ).distinct()

        paginator = PostPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostViewSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)



class PostDetailView(APIView):
    """
        View for retrieving and deleting a specific post by its ID.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Post"],
        summary="Retrieve a single post",
        description="Get the details of a single post by ID.",
        responses={
            200: OpenApiResponse(description='Post retrieved successfully', response=PostViewSerializer),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
            404: OpenApiResponse(description='Post not found'),
        }
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('categories', 'tags', 'author').get(id=post_id)
            serializer = PostViewSerializer(post)

            return generate_response(status.HTTP_200_OK, "Post retrieved successfully", serializer.data)
        
        except Post.DoesNotExist:
            return generate_response(status.HTTP_404_NOT_FOUND, "Post not found", None)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred while retrieving the post: {str(e)}", None)


    @extend_schema(
        tags=["Post"],
        summary="Delete a post",
        description="Delete a post by ID. Users can only delete their own posts.",
        responses={
            204: OpenApiResponse(description='Post deleted successfully'),
            403: OpenApiResponse(description='Forbidden: You are not authorized to delete this post'),
            404: OpenApiResponse(description='Post not found'),
        },
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            if post.author != request.user:
                return generate_response(status.HTTP_403_FORBIDDEN, "You are not authorized to delete this post", None)
            
            post.delete()

            return generate_response(status.HTTP_200_OK, "Post deleted successfully", None)

        except Post.DoesNotExist:
            return generate_response(status.HTTP_404_NOT_FOUND, "Post not found", None)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred while deleting the post: {str(e)}", None)

    @extend_schema(
        tags=["Post"],
        summary="Update a post",
        description="Update a post by ID. Users can only update their own posts. This is a full replacement (PUT).",
        request=PostUpdateSerializer,
        responses={
            200: OpenApiResponse(description='Post updated successfully', response=PostViewSerializer),
            403: OpenApiResponse(description='Forbidden: You are not authorized to update this post'),
            404: OpenApiResponse(description='Post not found'),
        }
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            if post.author != request.user:
                return generate_response(status.HTTP_403_FORBIDDEN, "You are not authorized to update this post", None)

            serializer = PostUpdateSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_post = serializer.save()

            response_serializer = PostViewSerializer(updated_post)
            return generate_response(status.HTTP_200_OK, "Post updated successfully", response_serializer.data)

        except Post.DoesNotExist:
            return generate_response(status.HTTP_404_NOT_FOUND, "Post not found", None)

        except Exception as e:
            return generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred while updating the post: {str(e)}", None)




