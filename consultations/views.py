from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consultation, MedicalRecord, Prescription, PrescriptionItem
from .forms import ConsultationForm, MedicalRecordForm, PrescriptionForm, PrescriptionItemForm
from inventory.models import InventoryMedicine
import json


@login_required(login_url='/login/')
def consultation_list(request):
    consultations = Consultation.objects.select_related(
        'patient', 'doctor', 'prescription'
    ).all()
    return render(request, 'consultations/consultation_list.html', {'consultations': consultations})


@login_required(login_url='/login/')
def consultation_add(request):
    form = ConsultationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consultation added successfully.')
        return redirect('consultation_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Add Consultation',
        'back_url': 'consultation_list'
    })


@login_required(login_url='/login/')
def consultation_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    form = ConsultationForm(request.POST or None, instance=consultation)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consultation updated successfully.')
        return redirect('consultation_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Edit Consultation',
        'back_url': 'consultation_list'
    })


@login_required(login_url='/login/')
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        messages.success(request, 'Consultation deleted successfully.')
        return redirect('consultation_list')
    return render(request, 'consultations/confirm_delete.html', {
        'item': f"Consultation #{consultation.consultation_id}"
    })


@login_required(login_url='/login/')
def prescription_list(request):
    prescriptions = Prescription.objects.select_related('patient', 'doctor').all()
    return render(request, 'consultations/prescription_list.html', {'prescriptions': prescriptions})


@login_required(login_url='/login/')
def prescription_add(request):
    form = PrescriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Prescription added successfully.')
        return redirect('prescription_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Add Prescription',
        'back_url': 'prescription_list'
    })


@login_required(login_url='/login/')
def prescription_edit(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    form = PrescriptionForm(request.POST or None, instance=prescription)
    if form.is_valid():
        form.save()
        messages.success(request, 'Prescription updated successfully.')
        return redirect('prescription_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Edit Prescription',
        'back_url': 'prescription_list'
    })


@login_required(login_url='/login/')
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully.')
        return redirect('prescription_list')
    return render(request, 'consultations/confirm_delete.html', {
        'item': f"Prescription #{prescription.prescription_id}"
    })


@login_required(login_url='/login/')
def medical_record_list(request):
    records = MedicalRecord.objects.select_related('patient', 'doctor').all()
    return render(request, 'consultations/medical_record_list.html', {'records': records})


@login_required(login_url='/login/')
def medical_record_add(request):
    form = MedicalRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Medical record added successfully.')
        return redirect('medical_record_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Add Medical Record',
        'back_url': 'medical_record_list'
    })


@login_required(login_url='/login/')
def medical_record_edit(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    form = MedicalRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, 'Medical record updated successfully.')
        return redirect('medical_record_list')
    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Edit Medical Record',
        'back_url': 'medical_record_list'
    })


@login_required(login_url='/login/')
def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Medical record deleted successfully.')
        return redirect('medical_record_list')
    return render(request, 'consultations/confirm_delete.html', {
        'item': f"Record #{record.record_id}"
    })


@login_required(login_url='/login/')
def prescription_item_list(request):
    items = PrescriptionItem.objects.select_related(
        'prescription',
        'prescription__patient',
        'medicine'
    ).all()
    return render(request, 'consultations/prescription_item_list.html', {'items': items})


@login_required(login_url='/login/')
def prescription_item_add(request):
    form = PrescriptionItemForm(request.POST or None)
    medicine_prices = {
        str(med.pk): str(med.unit_price)
        for med in InventoryMedicine.objects.all().order_by('medicine_name')
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Prescription item added successfully.')
        return redirect('prescription_item_list')

    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Add Prescription Item',
        'back_url': 'prescription_item_list',
        'medicine_prices_json': json.dumps(medicine_prices),
    })


@login_required(login_url='/login/')
def prescription_item_edit(request, pk):
    item = get_object_or_404(PrescriptionItem, pk=pk)
    form = PrescriptionItemForm(request.POST or None, instance=item)
    medicine_prices = {
        str(med.pk): str(med.unit_price)
        for med in InventoryMedicine.objects.all().order_by('medicine_name')
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Prescription item updated successfully.')
        return redirect('prescription_item_list')

    return render(request, 'consultations/form.html', {
        'form': form,
        'title': 'Edit Prescription Item',
        'back_url': 'prescription_item_list',
        'medicine_prices_json': json.dumps(medicine_prices),
    })


@login_required(login_url='/login/')
def prescription_item_delete(request, pk):
    item = get_object_or_404(PrescriptionItem, pk=pk)
    if request.method == 'POST':
        prescription = item.prescription
        medicine = item.medicine

        medicine.quantity += item.quantity
        medicine.save(update_fields=['quantity'])

        item.delete()

        prescription.total_items = prescription.prescriptionitem_set.count()
        prescription.save(update_fields=['total_items'])

        messages.success(request, 'Prescription item deleted successfully.')
        return redirect('prescription_item_list')

    return render(request, 'consultations/confirm_delete.html', {
        'item': f"Prescription Item #{item.prescription_item_id}"
    })