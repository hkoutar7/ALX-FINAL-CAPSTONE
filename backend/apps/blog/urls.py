from django.urls import path

from apps.blog.views import PostListCreateView, PostListPaginationView, PostByCategoryView, PostByAuthorView, PostSearchView, PostDetailView


urlpatterns = [
    path('v1/posts', PostListCreateView.as_view(), name='post-list-create'),
    path('v2/posts', PostListPaginationView.as_view(), name='post-list'),
    path('v1/posts/category/<int:category_id>', PostByCategoryView.as_view(), name='posts_by_category'),
    path('v1/posts/author/<int:author_id>', PostByAuthorView.as_view(), name='posts_by_author'),
    path('v1/posts/search', PostSearchView.as_view(), name='post-search'),
    path('v1/posts/<int:post_id>', PostDetailView.as_view(), name='post-detail-update-delete'),
]


