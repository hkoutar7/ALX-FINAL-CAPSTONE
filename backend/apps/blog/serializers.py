from rest_framework import serializers

from apps.blog.models import Post, Category, Tag, PostCategory
from apps.users.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class PostCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = PostCategory
        fields = ['id', 'category']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PostViewSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    post_categories = PostCategorySerializer(many=True, source='categories')

    class Meta:
        model = Post
        fields = [ 'id', 'title', 'content', 'status', 'author', 'post_categories', 'tags']













# # Category Serializer (View Only)
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description']

# # Tag Serializer (View Only)
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name']

# # Post Creation Serializer
# class PostCreateSerializer(serializers.ModelSerializer):
#     categories = serializers.ListField(
#         child=serializers.IntegerField(), write_only=True
#     )  # Accept category IDs as a list
#     tags = serializers.ListField(
#         child=serializers.CharField(), write_only=True
#     )  # Accept tags as a list of strings

#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'status', 'categories', 'tags']

#     def validate_categories(self, category_ids):
#         # Validate categories exist
#         if not Category.objects.filter(id__in=category_ids).exists():
#             raise serializers.ValidationError("One or more category IDs are invalid.")
#         return category_ids

#     def validate_tags(self, tags):
#         # Ensure tags are unique
#         if len(tags) != len(set(tags)):
#             raise serializers.ValidationError("Duplicate tags are not allowed.")
#         return tags

#     def create(self, validated_data):
#         categories = validated_data.pop('categories', [])
#         tags = validated_data.pop('tags', [])

#         post = Post.objects.create(**validated_data)

#         # Associate categories
#         PostCategory.objects.bulk_create(
#             [PostCategory(post=post, category_id=cat_id) for cat_id in categories]
#         )

#         # Create tags
#         Tag.objects.bulk_create([Tag(post=post, name=tag) for tag in tags])

#         return post



# class PostViewSerializer(serializers.ModelSerializer):
#     # Example of incorrect usage:
#     categories = serializers.ListSerializer(child=serializers.CharField(), source='categories')

#     # Correct usage:
#     categories = serializers.ListSerializer(child=serializers.CharField())

#     class Meta:
#         model = Post
#         fields = '__all__'
