from django.urls import path
from .views import ProductListAPIView, ProductDetailView

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('/<int:package_id>', ProductDetailView.as_view()),
]