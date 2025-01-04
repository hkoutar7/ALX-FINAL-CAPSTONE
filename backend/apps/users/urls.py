from django.urls import path

from apps.users.viewsAuth import LoginView, RegisterView, UserProfileView
from apps.users.viewsUserManagment import UsersListView, UserDetailView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('me', UserProfileView.as_view(), name='user-profile'),

    path('users', UsersListView.as_view(), name='users-list'),
    path('users/<int:id>', UserDetailView.as_view(), name='user-detail'),
    
]
