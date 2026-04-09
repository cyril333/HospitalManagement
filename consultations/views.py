from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Consultation, MedicalRecord, Prescription, PrescriptionItem
from .forms import ConsultationForm, MedicalRecordForm, PrescriptionForm, PrescriptionItemForm

@login_required(login_url='/login/')
def consultation_list(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultations/consultation_list.html', {'consultations': consultations})

@login_required(login_url='/login/')
def consultation_add(request):
    form = ConsultationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('consultation_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Add Consultation', 'back_url': 'consultation_list'})

@login_required(login_url='/login/')
def consultation_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    form = ConsultationForm(request.POST or None, instance=consultation)
    if form.is_valid():
        form.save()
        return redirect('consultation_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Edit Consultation', 'back_url': 'consultation_list'})

@login_required(login_url='/login/')
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        return redirect('consultation_list')
    return render(request, 'consultations/confirm_delete.html', {'item': f"Consultation #{consultation.consultation_id}"})

@login_required(login_url='/login/')
def prescription_list(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'consultations/prescription_list.html', {'prescriptions': prescriptions})

@login_required(login_url='/login/')
def prescription_add(request):
    form = PrescriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('prescription_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Add Prescription', 'back_url': 'prescription_list'})

@login_required(login_url='/login/')
def prescription_edit(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    form = PrescriptionForm(request.POST or None, instance=prescription)
    if form.is_valid():
        form.save()
        return redirect('prescription_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Edit Prescription', 'back_url': 'prescription_list'})

@login_required(login_url='/login/')
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        return redirect('prescription_list')
    return render(request, 'consultations/confirm_delete.html', {'item': f"Prescription #{prescription.prescription_id}"})

@login_required(login_url='/login/')
def medical_record_list(request):
    records = MedicalRecord.objects.all()
    return render(request, 'consultations/medical_record_list.html', {'records': records})

@login_required(login_url='/login/')
def medical_record_add(request):
    form = MedicalRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('medical_record_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Add Medical Record', 'back_url': 'medical_record_list'})

@login_required(login_url='/login/')
def medical_record_edit(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('medical_record_list')
    return render(request, 'consultations/form.html', {'form': form, 'title': 'Edit Medical Record', 'back_url': 'medical_record_list'})

@login_required(login_url='/login/')
def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('medical_record_list')
    return render(request, 'consultations/confirm_delete.html', {'item': f"Record #{record.record_id}"})