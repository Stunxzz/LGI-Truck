from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from users.forms import CustomAuthenticationForm, CustomUserCreationForm
from users.models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)




class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not CustomUser.objects.exists():
                user.role = 'admin'
                user.is_staff = True
                user.is_superuser = True

            user.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('delivery_note_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'register.html', {'form': form})





class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
