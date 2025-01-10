from rest_framework import serializers

from apps.blog.models import Post, Category, Tag, PostCategory
from apps.users.models import User


# View Serialisers 

class CategoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class PostCategoryViewSerializer(serializers.ModelSerializer):
    category = CategoryViewSerializer()

    class Meta:
        model = PostCategory
        fields = ['id', 'category']


class TagViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class AuthorViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PostViewSerializer(serializers.ModelSerializer):
    author = AuthorViewSerializer()
    tags = TagViewSerializer(many=True)
    post_categories = PostCategoryViewSerializer(many=True, source='categories')

    class Meta:
        model = Post
        fields = [ 'id', 'title', 'content', 'status', 'author', 'post_categories', 'tags']


# Create Serialisers 

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostCategoryCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = PostCategory
        fields = ['category_id']


class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True)
    post_categories = PostCategoryCreateSerializer(many=True, source='categories')

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'post_categories', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories_data = validated_data.pop('categories', [])
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            Tag.objects.create(post=post, **tag_data)

        for category_data in categories_data:
            category = Category.objects.get(id=category_data['category_id'])
            PostCategory.objects.create(post=post, category=category)

        return post


# Update Serialisers 

class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True)
    post_categories = PostCategoryCreateSerializer(many=True, source='categories')

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'post_categories', 'tags']

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories_data = validated_data.pop('categories', [])

        instance.title = validated_data.get('title', None)
        instance.content = validated_data.get('content', None)
        instance.status = validated_data.get('status', None)
        instance.save()

        instance.tags.all().delete()
        for tag_data in tags_data:
            Tag.objects.create(post=instance, **tag_data)

        instance.categories.all().delete()
        for category_data in categories_data:
            category = Category.objects.get(id=category_data['category_id'])
            PostCategory.objects.create(post=instance, category=category)

        return instance
