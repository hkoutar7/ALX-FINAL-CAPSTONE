from django.db import models
from apps.users.models import User


class PostStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PUBLISHED = 'PUBLISHED', 'Published'


class Post(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', db_index=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        """
            Return a string representation of the post.
        """
        return f"Post: {self.title} by {self.author.username}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        """
            Return a string representation of the category.
        """
        return f"Category: {self.name}"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_categories'

    def __str__(self):
        """
            Return a string representation of the post-category relation.
        """
        return f"Post '{self.post.title}' belongs to Category '{self.category.name}'"


class Tag(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        db_table = 'tags'

    def __str__(self):
        """
            Return a string representation of the tag.
        """
        return f"Tag: {self.name} for Post '{self.post.title}'"
