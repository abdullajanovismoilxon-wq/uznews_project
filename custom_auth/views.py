import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

from .forms import CustomUserCreationForm
from .models import User, EmailVerification


def send_verification_code(user):
    code = str(random.randint(100000, 999999))
    expires = timezone.now() + timedelta(minutes=10)

    EmailVerification.objects.create(
        user=user,
        verification_code=code,
        expires_at=expires
    )

    send_mail(
        subject="Tasdiqlash kodi",
        message=f"Sizning tasdiqlash kodingiz: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # tasdiqlanmaguncha aktiv emas
            user.save()
            send_verification_code(user)
            request.session['user_id'] = user.id
            return redirect("custom_auth:verify_email")
    else:
        form = CustomUserCreationForm()
    return render(request, "custom_auth/register.html", {"form": form})


def verify_email(request):
    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("user_id")
        user = User.objects.get(id=user_id)
        try:
            verification = EmailVerification.objects.filter(
                user=user,
                verification_code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('expires_at')
        except EmailVerification.DoesNotExist:
            return render(request, "custom_auth/verify_email.html", {"error": "Kod noto‘g‘ri yoki muddati tugagan"})

        verification.is_used = True
        verification.save()
        user.is_active = True
        user.is_verified = True
        user.save()

        login(request, user)
        request.session.set_expiry(86400)  # 1 kun
        return redirect("blogapp:post_list")

    return render(request, "custom_auth/verify_email.html")


def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, "custom_auth/login.html", {"error": "Email yoki parol noto‘g‘ri"})

        login(request, user)
        request.session.set_expiry(86400)  # 1 kun
        return redirect("blogapp:post_list")

    return render(request, "custom_auth/login.html")



def custom_logout(request):
    logout(request)
    return redirect("custom_auth:login")
