from django.urls import path
from .views import CategoryAPiView

urlpatterns = [
    path('category/', CategoryAPiView.as_view()),
]
