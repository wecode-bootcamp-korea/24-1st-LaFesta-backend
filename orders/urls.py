from django.urls import path
from           . import views

urlpatterns = [
    path("/cart", views.CartView.as_view()),
    path("/order", views.OrderView.as_view()),
    path("/order-information", views.OrderInformationView.as_view()),
]
