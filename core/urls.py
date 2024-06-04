from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings
from oauth.views import OAuthAuthorizationView, OAuthCallbackView

urlpatterns = [
    path("api/", include("api.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("tinymce/", include("tinymce.urls")),
    path("hemis/authorization/", OAuthAuthorizationView.as_view(), name="hemis_login"),
    path("hemis/callback/", OAuthCallbackView.as_view(), name="hemis_callback"),
]

urlpatterns += i18n_patterns(  # Публикации
    path("super-admin/", admin.site.urls),  # Супер админка
    path("posts/", include("posts.urls_public")),  # Статьи
    path("categories/", include("category.urls_public")),  # Категории
    path("kpi/", include("home.urls_public")),  # Пользователь
    path("auth/", include("oauth.urls")),
    path("administrator/", include("core.urls_admin")),  # Админка
    path("", include("index.urls_public")),  # Главная страница
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
