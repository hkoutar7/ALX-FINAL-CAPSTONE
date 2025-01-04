from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.users.serializers import UserCreateSerializer, LoginSerializer, UserViewSerializer



class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [BasicAuthentication]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description='Login successful'),
            400: OpenApiResponse(description='Invalid credentials')
        })
    def post(self, request):
        """
        Login user and return success message
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "status_code": 200,
                "message": "Login successful",
                "data": UserViewSerializer(user).data
            })
        return Response({
            "status_code": 400,
            "message": "Invalid credentials",
            "data": {}
        }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserCreateSerializer,
        responses={
            201: OpenApiResponse(description='User successfully registered'),
            400: OpenApiResponse(description='Registration failed')
        })
    def post(self, request):
        """
        Register a new user
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status_code": 201,
                "message": "User registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status_code": 400,
            "message": "User registration failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description='User profile details', response=UserViewSerializer),
            400: OpenApiResponse(description='Authentication failed or invalid credentials'),
        }
    )
    def get(self, request):
        """
        Retrieve the user profile
        """
        try:
            user = request.user
            if not user or not user.is_authenticated:
                raise AuthenticationFailed("Invalid credentials or not authenticated.")

            # Serialize user data
            serializer = UserViewSerializer(user)
            return Response({
                "status_code": 200,
                "message": "User profile retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({
                "status_code": 400,
                "message": str(e),
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)



