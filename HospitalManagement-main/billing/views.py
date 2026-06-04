import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Billing
from .forms import BillingForm
from admissions.models import Admission
from consultations.models import Prescription, PrescriptionItem


@login_required(login_url='/login/')
def billing_home(request):
    bills = Billing.objects.select_related('patient').all().order_by('-bill_date', '-bill_id')
    bills_count = bills.count()
    unpaid_count = bills.filter(payment_status__in=['Unpaid', 'Partially Paid']).count()

    return render(request, 'billing/billing_home.html', {
        'bills_count': bills_count,
        'unpaid_count': unpaid_count,
    })


@login_required(login_url='/login/')
def billing_list(request):
    bills = Billing.objects.select_related(
        'patient', 'admission', 'consultation', 'prescription'
    ).all().order_by('-bill_date', '-bill_id')
    return render(request, 'billing/billing_list.html', {'bills': bills})


@login_required(login_url='/login/')
def billing_detail(request, pk):
    bill = get_object_or_404(
        Billing.objects.select_related('patient', 'admission', 'consultation', 'prescription'),
        pk=pk
    )
    return render(request, 'billing/billing_detail.html', {'bill': bill})


@login_required(login_url='/login/')
def billing_add(request):
    form = BillingForm(request.POST or None)
    billing_data = _build_billing_data()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill added successfully.')
            return redirect('billing_list')

    return render(request, 'billing/form.html', {
        'form': form,
        'title': 'Add Bill',
        'back_url': 'billing_list',
        'billing_data_json': json.dumps(billing_data)
    })


@login_required(login_url='/login/')
def billing_edit(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    form = BillingForm(request.POST or None, instance=bill)
    billing_data = _build_billing_data()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated successfully.')
            return redirect('billing_list')

    return render(request, 'billing/form.html', {
        'form': form,
        'title': 'Edit Bill',
        'back_url': 'billing_list',
        'billing_data_json': json.dumps(billing_data)
    })


@login_required(login_url='/login/')
def billing_delete(request, pk):
    bill = get_object_or_404(Billing, pk=pk)

    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill deleted successfully.')
        return redirect('billing_list')

    return render(request, 'billing/confirm_delete.html', {
        'item': f"Bill #{bill.bill_id}"
    })


def _get_billing_end_datetime(admission, manual_admitted_out=None, payment_status=None):
    if not admission or not admission.admitted_in:
        return None

    if manual_admitted_out:
        return manual_admitted_out

    if admission.admitted_out:
        return admission.admitted_out

    if payment_status == 'Paid':
        return None

    if admission.status == 'Active':
        return timezone.now()

    return None


def _calculate_stay_days(admission, manual_admitted_out=None, payment_status=None):
    if not admission or not admission.admitted_in:
        return 0

    billing_end = _get_billing_end_datetime(admission, manual_admitted_out, payment_status)

    if not billing_end:
        return 0

    duration = billing_end - admission.admitted_in
    days = duration.days

    if duration.seconds > 0:
        days += 1

    if days <= 0:
        days = 1

    return days


def _build_billing_data():
    data = {
        'admissions': {},
        'prescriptions': {}
    }

    admissions = Admission.objects.select_related('attending_doctor', 'room').all()
    for admission in admissions:
        days = _calculate_stay_days(admission)

        doctor_rate = Decimal('0.00')
        room_rate = Decimal('0.00')
        doctor_charge = Decimal('0.00')
        room_charge = Decimal('0.00')
        total_charge = Decimal('0.00')
        is_tentative = False

        if admission.attending_doctor and admission.attending_doctor.daily_rate is not None:
            doctor_rate = admission.attending_doctor.daily_rate

        if admission.room and admission.room.daily_rate is not None:
            room_rate = admission.room.daily_rate

        if days > 0:
            doctor_charge = doctor_rate * Decimal(days)
            room_charge = room_rate * Decimal(days)
            total_charge = doctor_charge + room_charge

        if admission.status == 'Active' and not admission.admitted_out:
            is_tentative = True

        data['admissions'][str(admission.pk)] = {
            'patient_id': str(admission.patient_id),
            'admitted_in': admission.admitted_in.strftime('%Y-%m-%dT%H:%M') if admission.admitted_in else '',
            'saved_admitted_out': admission.admitted_out.strftime('%Y-%m-%dT%H:%M') if admission.admitted_out else '',
            'status': admission.status,
            'is_tentative': is_tentative,
            'days': days,
            'doctor_rate': str(doctor_rate),
            'room_rate': str(room_rate),
            'doctor_charge': str(doctor_charge),
            'room_charge': str(room_charge),
            'room_type': admission.room.room_type if admission.room else '',
            'charge': str(total_charge)
        }

    prescriptions = Prescription.objects.all()
    for prescription in prescriptions:
        total = PrescriptionItem.objects.filter(
            prescription=prescription
        ).aggregate(total=Sum('unit_price'))['total'] or Decimal('0.00')

        data['prescriptions'][str(prescription.pk)] = {
            'patient_id': str(prescription.patient_id),
            'charge': str(total)
        }

    return data