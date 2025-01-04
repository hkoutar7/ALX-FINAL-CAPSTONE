from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from datetime import datetime

from apps.users.serializers import UserViewSerializer, UserUpdateSerializer
from apps.users.models import User


class UsersListView(APIView):
    """
        Retrieve a list of all users.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User Management"],
        summary="Retrieve all users",
        description="Get a list of all registered users.",
        responses={
            200: OpenApiResponse(description='List of all users', response=UserViewSerializer(many=True)),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserViewSerializer(users, many=True)
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "Users retrieved successfully",
                "timestamp": datetime.now(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while retrieving users.",
                "timestamp": datetime.now(),
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserDetailView(APIView):
    """
        View, Update, Delete a user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User Management"],
        summary="Retrieve user details",
        description="Get details of a specific user by their ID.",
        responses={
            200: OpenApiResponse(description='User details retrieved successfully', response=UserViewSerializer),
            404: OpenApiResponse(description='User not found'),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserViewSerializer(user)
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "User details retrieved successfully",
                "timestamp": datetime.now(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found.",
                "timestamp": datetime.now(),
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while retrieving the user details.",
                "timestamp": datetime.now(),
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        tags=["User Management"],
        summary="Delete a user",
        description="Delete a specific user by their ID.",
        responses={
            200: OpenApiResponse(description='User deleted successfully'),
            404: OpenApiResponse(description='User not found'),
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "User deleted successfully",
                "timestamp": datetime.now(),
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found.",
                "timestamp": datetime.now(),
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while deleting the user.",
                "timestamp": datetime.now(),
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        tags=["User Management"],
        summary="Update user details",
        request=UserUpdateSerializer,
        description="Update the first name, last name, email, and username of a specific user.",
        responses={
            200: OpenApiResponse(description='User details updated successfully'),
            400: OpenApiResponse(description='Validation error'),
            404: OpenApiResponse(description='User not found'),
        }
    )
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)

            serializer = UserUpdateSerializer(instance=user, data=request.data, context={'user_id': user.id})

            if not serializer.is_valid():
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation error",
                    "timestamp": datetime.now(),
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "User updated successfully",
                "timestamp": datetime.now(),
                "data": UserViewSerializer(user).data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found.",
                "timestamp": datetime.now(),
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while updating the user details.",
                "error": str(e),
                "timestamp": datetime.now(),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


