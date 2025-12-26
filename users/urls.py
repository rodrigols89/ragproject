from django.urls import path

from . import views

urlpatterns = [
    path(
        route="",
        view=views.login_view,
        name="index"
    ),
    path(
        route="home/",
        view=views.home_view,
        name="home"
    ),
    path(
        route="logout/",
        view=views.logout_view,
        name="logout"
    ),
    path(
        route="create-account/",
        view=views.create_account,
        name="create-account"
    ),
]
