from django.urls import path

from users.views import KakaoLogInView, RenewalingToken

urlpatterns = [
    path('/kakao-login', KakaoLogInView.as_view()),
    path('/refresh-token', RenewalingToken.as_view()),
]

