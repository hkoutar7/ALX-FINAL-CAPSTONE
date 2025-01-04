from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from apps.users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating a new user. 
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
            Create and return a new user instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer for updating an existing user's details.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        """
            Validate the uniqueness of `email` and `username` fields during updates.
        """
        user_id = self.context.get('user_id')

        email = attrs.get('email')
        if email and User.objects.filter(email=email).exclude(id=user_id).exists():
            raise serializers.ValidationError({"email": "This email is already in use by another user."})

        username = attrs.get('username')
        if username and User.objects.filter(username=username).exclude(id=user_id).exists():
            raise serializers.ValidationError({"username": "This username is already in use by another user."})

        return attrs


class LoginSerializer(serializers.Serializer):
    """
        Serializer for user login.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
            Validate user credentials.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user


class UserViewSerializer(serializers.ModelSerializer):
    """
        Serializer for viewing user details.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
