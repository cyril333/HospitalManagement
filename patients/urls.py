from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_add, name='patient_add'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),
]