from django.contrib import admin
from django.urls import path

from pages.views import home_view, contact_view
from products.views import (
  product_detail_view,
  product_create_view,
  product_delete_view,
  product_list_view
)

app_name = 'products'
urlpatterns = [
  path('', product_list_view, name='product-list'),
  path('<int:id>/', product_detail_view, name='product-detail'),
  path('<int:id>/delete/', product_delete_view, name='product-delete'),
  path('create/', product_create_view, name='product-create')
]
