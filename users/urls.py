from users.views import SignUpView, LogInView, UserSearchView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="search"),
]
