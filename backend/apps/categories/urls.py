"""
URL configuration for categories app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Categories management
    path('categories/', views.list_categories_view, name='categories-list'),
    path('categories/create/', views.create_category_view, name='categories-create'),
    path('categories/<int:category_id>/', views.get_category_detail_view, name='category-detail'),
    path('categories/<int:category_id>/update/', views.update_category_view, name='category-update'),
    path('categories/<int:category_id>/delete/', views.delete_category_view, name='category-delete'),
]

