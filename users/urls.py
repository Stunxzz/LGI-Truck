from django.urls import path

from users.authentication_views.authentication_views import (
    RegisterView, LogoutView, CustomLoginView)  # Authentication VIEWS
from users.views import UserListView, UserEditView, ProfileView, CustomPasswordChangeView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
     path('users-list/', UserListView.as_view(), name='user_list'),
    path('user/edit/<int:pk>/', UserEditView.as_view(), name='user_edit'),

     path('profile/', ProfileView.as_view(), name='profile'),

    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
