from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(
        TemplateView.as_view(template_name='index.html'),
        login_url='/login/'
    ), name='index'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('edit-profile/', account_views.edit_profile, name='edit_profile'),
    path('accounts/', include('accounts.urls')),
    path('departments/', include('departments.urls')),
    path('patients/', include('patients.urls')),
    path('admissions/', include('admissions.urls')),
    path('consultations/', include('consultations.urls')),
    path('billing/', include('billing.urls')),
    path('inventory/', include('inventory.urls')),
]