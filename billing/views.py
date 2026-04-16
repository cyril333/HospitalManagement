from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Billing
from .forms import BillingForm

@login_required(login_url='/login/')
def billing_list(request):
    bills = Billing.objects.all()
    return render(request, 'billing/billing_list.html', {'bills': bills})

@login_required(login_url='/login/')
def billing_detail(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    return render(request, 'billing/billing_detail.html', {'bill': bill})

@login_required(login_url='/login/')
def billing_add(request):
    form = BillingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('billing_list')
    return render(request, 'billing/billing_form.html', {'form': form, 'title': 'Add Bill', 'back_url': 'billing_list'})

@login_required(login_url='/login/')
def billing_edit(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    form = BillingForm(request.POST or None, instance=bill)
    if form.is_valid():
        form.save()
        return redirect('billing_list')
    return render(request, 'billing/billing_form.html', {'form': form, 'title': 'Edit Bill', 'back_url': 'billing_list'})

@login_required(login_url='/login/')
def billing_delete(request, pk):
    bill = get_object_or_404(Billing, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('billing_list')
    return render(request, 'billing/confirm_delete.html', {'item': f"Bill #{bill.bill_id}"})