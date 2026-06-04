from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_list, name='admission_list'),
    path('add/', views.admission_add, name='admission_add'),
    path('edit/<int:pk>/', views.admission_edit, name='admission_edit'),
    path('delete/<int:pk>/', views.admission_delete, name='admission_delete'),
]