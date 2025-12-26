from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path(  # Rotas do django-allauth
        "accounts/",
        include("allauth.urls")
    ),
]
