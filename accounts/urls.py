from django.urls import path
from . import views

urlpatterns = [

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_add, name='doctor_add'),
    path('doctors/edit/<int:pk>/', views.doctor_edit, name='doctor_edit'),
    path('doctors/delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),
    path('nurses/', views.nurse_list, name='nurse_list'),
    path('nurses/add/', views.nurse_add, name='nurse_add'),
    path('nurses/edit/<int:pk>/', views.nurse_edit, name='nurse_edit'),
    path('nurses/delete/<int:pk>/', views.nurse_delete, name='nurse_delete'),
    path('addNewDoctor/', views.add_new_doctor, name='add_new_doctor'), #add new doctor
    path('addNewNurse/', views.add_new_nurse, name='add_new_nurse'), #add new nurse
]