from django.urls import path
from . import views

urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('add/', views.department_add, name='department_add'),
    path('edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('delete/<int:pk>/', views.department_delete, name='department_delete'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/edit/<int:pk>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),
    path('addNewDepartment/', views.add_new_department, name='add_new_department'), #add new departments
    path('addNewRoom/', views.add_new_room, name='add_new_room'), #add new rooms
]