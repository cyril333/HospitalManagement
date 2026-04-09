from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.BillingListView.as_view(), name='list'),
    path('<int:pk>/', views.BillingDetailView.as_view(), name='detail'),
    path('create/', views.BillingCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.BillingUpdateView.as_view(), name='update'),
]