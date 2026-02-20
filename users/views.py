from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings

from .forms import UserRegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка приветственного письма
        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию в нашем магазине!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.instance.email],
        )

        return response