from django.urls import path
from .           import views

urlpatterns = [
    path("/list", views.ProductListView.as_view()),
    path("/<int:product_id>", views.ProductDetailView.as_view())
]