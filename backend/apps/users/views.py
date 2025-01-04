from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.authentication import BaseAuthentication
from apps.users.serialisers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    """
        API for user registration
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [BaseAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "status_code": status.HTTP_201_CREATED,
            "message": "User registered successfully.",
            "timestamp": str(datetime.now()),
            "data": serializer.data
        })


@extend_schema(
    request=LoginSerializer,  # This will define the request body schema
    responses={200: OpenApiResponse(response=LoginSerializer)},  # Define the expected response
)
class LoginView(APIView):
    """
    API for user login
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "status_code": 200,
            "message": "Login successful.",
            "timestamp": str(datetime.now()),
            "data": serializer.validated_data
        })
