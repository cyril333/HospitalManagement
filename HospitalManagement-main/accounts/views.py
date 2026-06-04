from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import DoctorProfile, NurseProfile, UserProfile, AdminProfile
from .forms import DoctorForm, NurseForm
from functools import wraps


def user_is_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return UserProfile.objects.filter(user=user, role='Admin').exists()


def admin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        if not user_is_admin(request.user):
            return HttpResponseForbidden("Only admins can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if UserProfile.objects.filter(user=user, role='Admin').exists():
                admin_profile = AdminProfile.objects.filter(user=user).first()
                if admin_profile:
                    from django.utils import timezone
                    admin_profile.last_login = timezone.now()
                    admin_profile.save(update_fields=['last_login'])

            return redirect('index')
        else:
            error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()

        new_password = request.POST.get('password', '').strip()
        user.save()

        if new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

        messages.success(request, 'Profile updated successfully.')
        return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'user': user})


@admin_required
def doctor_list(request):
    doctors = DoctorProfile.objects.select_related('user', 'department').order_by('user__last_name', 'user__first_name')
    return render(request, 'accounts/doctor_list.html', {'doctors': doctors})


@admin_required
def doctor_add(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        admin_profile = AdminProfile.objects.filter(user=request.user).first()
        doctor = form.save(created_by_admin=admin_profile)
        messages.success(request, f'Doctor "{doctor}" added successfully.')
        return redirect('doctor_list')
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Add Doctor',
        'subtitle': 'Create a doctor account and complete their profile.',
        'back_url': 'doctor_list'
    })


@admin_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    form = DoctorForm(request.POST or None, instance=doctor)
    if form.is_valid():
        doctor = form.save()
        messages.success(request, f'Doctor "{doctor}" updated successfully.')
        return redirect('doctor_list')
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Edit Doctor',
        'subtitle': 'Update doctor account and profile details.',
        'back_url': 'doctor_list'
    })


@admin_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    if request.method == 'POST':
        doctor_name = str(doctor)
        doctor.delete()
        messages.success(request, f'Doctor "{doctor_name}" deleted successfully.')
        return redirect('doctor_list')
    return render(request, 'accounts/confirm_delete.html', {'item': str(doctor)})


@admin_required
def nurse_list(request):
    nurses = NurseProfile.objects.select_related('user', 'department').order_by('user__last_name', 'user__first_name')
    return render(request, 'accounts/nurse_list.html', {'nurses': nurses})


@admin_required
def nurse_add(request):
    form = NurseForm(request.POST or None)
    if form.is_valid():
        admin_profile = AdminProfile.objects.filter(user=request.user).first()
        nurse = form.save(created_by_admin=admin_profile)
        messages.success(request, f'Nurse "{nurse}" added successfully.')
        return redirect('nurse_list')
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Add Nurse',
        'subtitle': 'Create a nurse account and complete their profile.',
        'back_url': 'nurse_list'
    })


@admin_required
def nurse_edit(request, pk):
    nurse = get_object_or_404(NurseProfile, pk=pk)
    form = NurseForm(request.POST or None, instance=nurse)
    if form.is_valid():
        nurse = form.save()
        messages.success(request, f'Nurse "{nurse}" updated successfully.')
        return redirect('nurse_list')
    return render(request, 'accounts/form.html', {
        'form': form,
        'title': 'Edit Nurse',
        'subtitle': 'Update nurse account and profile details.',
        'back_url': 'nurse_list'
    })


@admin_required
def nurse_delete(request, pk):
    nurse = get_object_or_404(NurseProfile, pk=pk)
    if request.method == 'POST':
        nurse_name = str(nurse)
        nurse.delete()
        messages.success(request, f'Nurse "{nurse_name}" deleted successfully.')
        return redirect('nurse_list')
    return render(request, 'accounts/confirm_delete.html', {'item': str(nurse)})