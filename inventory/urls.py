from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_home, name='inventory_home'),  # ← ADD THIS

    # Medicine URLs
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/edit/<int:pk>/', views.medicine_edit, name='medicine_edit'),
    path('medicines/delete/<int:pk>/', views.medicine_delete, name='medicine_delete'),

    # Supplies URLs
    path('supplies/', views.supplies_list, name='supplies_list'),
    path('supplies/add/', views.supplies_add, name='supplies_add'),
    path('supplies/edit/<int:pk>/', views.supplies_edit, name='supplies_edit'),
    path('supplies/delete/<int:pk>/', views.supplies_delete, name='supplies_delete'),
]