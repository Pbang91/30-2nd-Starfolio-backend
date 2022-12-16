from django.urls import path

from users.views import KakaoLogInView, RenewalingToken, LogOutView

urlpatterns = [
    path('/kakao-login', KakaoLogInView.as_view(), name="kakao_login"),
    path('/refresh-token', RenewalingToken.as_view()),
    path('/logout', LogOutView.as_view(), name='logout')
]