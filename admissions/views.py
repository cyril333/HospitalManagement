from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Admission, AdmissionSupplyUsage
from .forms import AdmissionCreateForm, AdmissionEditForm, AdmissionSupplyUsageForm
from billing.models import Billing


@login_required(login_url='/login/')
def admission_list(request):
    admissions = Admission.objects.select_related(
        'patient', 'room', 'attending_doctor'
    ).all().order_by('-admission_id')
    return render(request, 'admissions/admission_list.html', {'admissions': admissions})


@login_required(login_url='/login/')
def admission_add(request):
    form = AdmissionCreateForm(request.POST or None)

    if form.is_valid():
        admission = form.save()

        Billing.objects.get_or_create(
            patient=admission.patient,
            admission=admission,
            defaults={
                'consultation': None,
                'prescription': None,
                'discount': 0,
                'payment_status': 'Unpaid',
            }
        )

        messages.success(request, 'Admission added successfully.')
        return redirect('admission_list')

    return render(request, 'admissions/form.html', {
        'form': form,
        'title': 'Add Admission',
        'back_url': 'admission_list'
    })


@login_required(login_url='/login/')
def admission_edit(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    form = AdmissionEditForm(request.POST or None, instance=admission)

    if form.is_valid():
        updated_admission = form.save()

        Billing.objects.get_or_create(
            patient=updated_admission.patient,
            admission=updated_admission,
            defaults={
                'consultation': None,
                'prescription': None,
                'discount': 0,
                'payment_status': 'Unpaid',
            }
        )

        messages.success(request, 'Admission updated successfully.')
        return redirect('admission_list')

    return render(request, 'admissions/form.html', {
        'form': form,
        'title': 'Edit Admission',
        'back_url': 'admission_list'
    })


@login_required(login_url='/login/')
def admission_delete(request, pk):
    admission = get_object_or_404(Admission, pk=pk)

    if request.method == 'POST':
        admission.delete()
        messages.success(request, 'Admission deleted successfully.')
        return redirect('admission_list')

    return render(request, 'admissions/confirm_delete.html', {
        'item': f"Admission #{admission.admission_id}"
    })