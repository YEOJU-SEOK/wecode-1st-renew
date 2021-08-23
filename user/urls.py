from django.urls import path, include
from .views import SingUpViewSet, Signin

urlpatterns = [
    path('signup/', SingUpViewSet.as_view()),
    path('/signin', Signin.as_view()),
]
