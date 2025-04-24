from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserEditForm, UserProfileForm


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.all()


class UserEditView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, f"User {form.instance.email} was successfully updated.")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)



class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)
