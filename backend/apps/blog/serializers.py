from rest_framework import serializers

from apps.blog.models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    """
        Used for receiving and validating client input.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'author']
        read_only_fields = ['author']



class PostViewSerializer(serializers.ModelSerializer):
    """
        Used for sending data to the client.
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'status', 'author']
