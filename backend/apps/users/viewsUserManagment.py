from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
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
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while retrieving the user details.",
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
                "message": "User deleted successfully"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while deleting the user.",
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
            403: OpenApiResponse(description='Forbidden: Authentication required'),
        }
    )
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            
            user_serializer = UserViewSerializer(user)

            new_user_data = UserUpdateSerializer(data=request.data)

            if not new_user_data.is_valid():
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation error",
                    "errors": new_user_data.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            validated_data = new_user_data.validated_data 

            user.first_name = validated_data.get('first_name', user.first_name)
            user.last_name = validated_data.get('last_name', user.last_name)
            user.email = validated_data.get('email', user.email)
            user.username = validated_data.get('username', user.username)
            user.save()

            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "User updated successfully",
                "data": user_serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while updating the user details.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
