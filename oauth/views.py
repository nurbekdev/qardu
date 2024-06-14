from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.views import APIView

from .client import OAuth2Client
from .models import Teacher, User


class OAuthAuthorizationView(APIView):

    def get(self, request):
        client = OAuth2Client(
            client_id=settings.OAUTH2_CLIENT_ID,
            client_secret=settings.OAUTH2_CLIENT_SECRET,
            redirect_uri=settings.OAUTH2_REDIRECT_URI,
            authorize_url=settings.OAUTH2_AUTHORIZE_URL,
            token_url=settings.OAUTH2_TOKEN_URL,
            resource_owner_url=settings.OAUTH2_USER_INFO_URL,
        )
        authorization_url = client.get_authorization_url()
        return redirect(authorization_url)


class OAuthCallbackView(APIView):
    template_name = "public/profile.html"

    def get(self, request, *args, **kwargs):
        print(request.GET)
        auth_code = request.GET.get("code")
        if not auth_code:
            return JsonResponse(
                {"error": "Authorization code is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        client = OAuth2Client(
            client_id=settings.OAUTH2_CLIENT_ID,
            client_secret=settings.OAUTH2_CLIENT_SECRET,
            redirect_uri=settings.OAUTH2_REDIRECT_URI,
            authorize_url=settings.OAUTH2_AUTHORIZE_URL,
            token_url=settings.OAUTH2_TOKEN_URL,
            resource_owner_url=settings.OAUTH2_USER_INFO_URL,
        )
        access_token_response = client.get_access_token(auth_code)

        if "access_token" in access_token_response:
            access_token = access_token_response["access_token"]
            user_details = client.get_user_details(access_token)

            if not user_details:
                return JsonResponse(
                    {"error": "Failed to obtain user details"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_teacher = False

            for role in user_details.get("roles", []):
                if role.get("code") == "teacher":
                    is_teacher = True
                    break

            if not is_teacher:
                messages.error(request, _("Пользователь не является учителем"))
                return redirect("oauth:login")

            if user_details.get("email") is None:
                messages.error(request, _("Не удалось получить адрес электронной почты"))
                return redirect("oauth:login")

            user, created = User.objects.get_or_create(
                teacher__uuid=user_details.get("uuid"),
                defaults={
                    "email": user_details.get("email"),
                    "first_name": user_details.get("firstname"),
                    "last_name": user_details.get("surname"),
                    "fathers_name": user_details.get("patronymic"),
                    "image_url": user_details.get("picture"),
                    "is_teacher": True,
                },
            )

            if created:
                Teacher.objects.create(
                    user=user,
                    uuid=user_details.get("uuid"),
                    status=1,
                )

            login(request, user)

            return redirect("/")
        else:
            return JsonResponse(
                {"error": "Failed to obtain access token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


def user_profile_view(request):
    return render(request, "public/profile.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index_public:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # clean email
        email = email.strip().lower()
        # clean password
        password = password.strip()

        user = User.objects.filter(email=email).first()
        if user:
            if user.check_password(password):
                login(request, user)
                return redirect("index_public:index")
            else:
                return render(
                    request, "public/login.html", {"error": "Неверный пароль"}
                )
        else:
            return render(
                request, "public/login.html", {"error": "Пользователь не найден"}
            )
    return render(request, "public/login.html", {})


def logout_view(request):
    logout(request)
    return redirect("index_public:index")
