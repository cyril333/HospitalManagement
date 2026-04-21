from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, NurseProfile
from .forms import DoctorForm, NurseForm

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
# New view for addNewDoctor URL
@login_required(login_url='/login/')
def add_new_doctor(request):
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('doctor_list')
    return render(request, 'accounts/addNewDoctor.html', {'form': form})

# New view for addNewNurse URL
@login_required(login_url='/login/')
def add_new_nurse(request):
    form = NurseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('nurse_list')
    return render(request, 'accounts/addNewNurse.html', {'form': form})