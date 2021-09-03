from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('<int:package_id>/', ProductDetailAPIView.as_view()),
]