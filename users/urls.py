from django.urls import path

from .views import create_account, login_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(
        route="create-account/",
        view=create_account,
        name="create-account"
    ),
]
