from django.urls import path
from . import views

urlpatterns = [
    path('', views.consultation_list, name='consultation_list'),
    path('add/', views.consultation_add, name='consultation_add'),
    path('edit/<int:pk>/', views.consultation_edit, name='consultation_edit'),
    path('delete/<int:pk>/', views.consultation_delete, name='consultation_delete'),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/add/', views.prescription_add, name='prescription_add'),
    path('prescriptions/edit/<int:pk>/', views.prescription_edit, name='prescription_edit'),
    path('prescriptions/delete/<int:pk>/', views.prescription_delete, name='prescription_delete'),
    path('records/', views.medical_record_list, name='medical_record_list'),
    path('records/add/', views.medical_record_add, name='medical_record_add'),
    path('records/edit/<int:pk>/', views.medical_record_edit, name='medical_record_edit'),
    path('records/delete/<int:pk>/', views.medical_record_delete, name='medical_record_delete'),
]