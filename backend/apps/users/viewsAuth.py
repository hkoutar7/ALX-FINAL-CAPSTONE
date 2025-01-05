from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime

from apps.users.serializers import UserCreateSerializer, LoginSerializer, UserViewSerializer


class LoginView(APIView):
    """
        User login endpoint to authenticate and return user data upon successful login.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Auth Management",
        description="Authenticate a user by logging them into the system.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description='Login successful', response=UserViewSerializer),
            400: OpenApiResponse(description='Invalid credentials')
        })
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                return Response({
                    "status_code": status.HTTP_200_OK,
                    "message": "Login successful",
                    "timestamp": datetime.now(),
                    "data": UserViewSerializer(user).data
                }, status=status.HTTP_200_OK)

            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid credentials",
                "timestamp": datetime.now(),
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while logging in the user.",
                "timestamp": datetime.now(),
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterView(APIView):
    """
        User registration endpoint to create a new user.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Auth Management",
        description="Register a user into the system.",
        request=UserCreateSerializer,
        responses={
            201: OpenApiResponse(description='User successfully registered'),
            400: OpenApiResponse(description='Registration failed')
        })
    def post(self, request):
        try:
            user_created = UserCreateSerializer(data=request.data)
            if user_created.is_valid():
                user = user_created.save()
                return Response({
                    "status_code": status.HTTP_201_CREATED,
                    "message": "User registered successfully",
                    "timestamp": datetime.now(),
                    "data": user_created.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "User registration failed",
                "timestamp": datetime.now(),
                "data": user_created.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while register in the user.",
                "timestamp": datetime.now(),
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserProfileView(APIView):
    """
        Retrieve the logged-in user's profile information.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Auth"],
        summary="Auth Management",
        description="Retrieve the profile information of an authenticated user.",
        responses={
            200: OpenApiResponse(description='User profile details', response=UserViewSerializer),
            400: OpenApiResponse(description='Authentication failed or invalid credentials'),
        }
    )
    def get(self, request):
        try:
            user = request.user
            if not user or not user.is_authenticated:
                raise AuthenticationFailed("Invalid credentials or not authenticated.")

            serializer = UserViewSerializer(user)
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": "User profile retrieved successfully",
                "timestamp": datetime.now(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "timestamp": datetime.now(),
            }, status=status.HTTP_400_BAD_REQUEST)


