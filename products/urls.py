from django.urls import path
from . import views

urlpatterns = [
    path("/<int:product_id>", views.ProductDetailView.as_view()),
    path("", views.ProductListView.as_view()),
    path("/search", views.SearchView.as_view()),
]
