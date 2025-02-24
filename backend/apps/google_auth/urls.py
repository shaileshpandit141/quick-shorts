from django.urls import path

from .views import GoogleCallbackView, GoogleLoginView

urlpatterns = [
    path("google/signin/", GoogleLoginView.as_view(), name="google-login"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google-callback"),
]
