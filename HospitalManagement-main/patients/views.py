from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm

@login_required(login_url='/login/')
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required(login_url='/login/')
def patient_add(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patient_list')
    return render(request, 'patients/form.html', {'form': form, 'title': 'Add Patient', 'back_url': 'patient_list'})

@login_required(login_url='/login/')
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patient_list')
    return render(request, 'patients/form.html', {'form': form, 'title': 'Edit Patient', 'back_url': 'patient_list'})

@login_required(login_url='/login/')
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/confirm_delete.html', {'item': patient.patient_name})