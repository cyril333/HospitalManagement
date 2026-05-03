from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout  # ← ADD THIS
from .models import DoctorProfile, NurseProfile
from .forms import DoctorForm, NurseForm


# --- AUTH VIEWS ---

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        new_password = request.POST.get('password', '')
        if new_password:
            user.set_password(new_password)
            login(request, user)
        user.save()
        return redirect('index')
    return render(request, 'edit_profile.html', {'user': user})


# --- DOCTOR VIEWS ---

@login_required(login_url='/login/')
def doctor_list(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'accounts/doctor_list.html', {'doctors': doctors})


@login_required(login_url='/login/')
def doctor_add(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('doctor_list')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Add Doctor', 'back_url': 'doctor_list'})


@login_required(login_url='/login/')
def doctor_edit(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    form = DoctorForm(request.POST or None, instance=doctor)
    if form.is_valid():
        form.save()
        return redirect('doctor_list')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Edit Doctor', 'back_url': 'doctor_list'})


@login_required(login_url='/login/')
def doctor_delete(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'accounts/confirm_delete.html', {'item': doctor.user.get_full_name()})


# --- NURSE VIEWS ---

@login_required(login_url='/login/')
def nurse_list(request):
    nurses = NurseProfile.objects.all()
    return render(request, 'accounts/nurse_list.html', {'nurses': nurses})


@login_required(login_url='/login/')
def nurse_add(request):
    form = NurseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('nurse_list')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Add Nurse', 'back_url': 'nurse_list'})


@login_required(login_url='/login/')
def nurse_edit(request, pk):
    nurse = get_object_or_404(NurseProfile, pk=pk)
    form = NurseForm(request.POST or None, instance=nurse)
    if form.is_valid():
        form.save()
        return redirect('nurse_list')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Edit Nurse', 'back_url': 'nurse_list'})


@login_required(login_url='/login/')
def nurse_delete(request, pk):
    nurse = get_object_or_404(NurseProfile, pk=pk)
    if request.method == 'POST':
        nurse.delete()
        return redirect('nurse_list')
    return render(request, 'accounts/confirm_delete.html', {'item': nurse.user.get_full_name()})