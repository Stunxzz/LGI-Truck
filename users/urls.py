from django.urls import path

from users.authentication_views.authentication_views import (
    RegisterView, LogoutView, CustomLoginView)  # Authentication VIEWS


urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]