from django.urls import path
from .views import ShoppingCartAPIView, CartDetailView

urlpatterns = [
    path('test/', ShoppingCartAPIView.as_view()),
    path('/cart/<int:cart_id>',CartDetailView.as_view())  
]
