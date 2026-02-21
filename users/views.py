from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

# Импортируем формы и модель
try:
    from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
    from .models import User
except ImportError as e:
    # Если есть ошибка импорта, выведем её
    print(f"Ошибка импорта в users/views.py: {e}")
    # Создадим заглушки
    UserRegisterForm = None
    UserLoginForm = None
    UserProfileForm = None
    User = None


class RegisterView(CreateView):
    """Контроллер регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка приветственного письма
        send_mail(
            subject='Добро пожаловать в наш магазин!',
            message=f'Уважаемый {self.object.email}, спасибо за регистрацию!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        return response


class UserLoginView(LoginView):
    """Контроллер авторизации"""
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        # Перенаправляем на главную страницу продуктов
        return reverse_lazy('products:product_list')


class UserLogoutView(LogoutView):
    """Контроллер выхода"""
    next_page = reverse_lazy('products:product_list')


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер профиля"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')