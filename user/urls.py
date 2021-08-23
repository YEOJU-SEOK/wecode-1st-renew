from django.urls import path, include
from .views import SingUpViewSet, SignInViewSet
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', SingUpViewSet.as_view()),
    path('signin/', SignInViewSet),
    path('api-token-auth/', obtain_jwt_token)
]
