from django.urls import path

from apps.blog.views import PostListCreateView


urlpatterns = [
    # path('posts/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('posts', PostListCreateView.as_view(), name='post-list-create'),
]


