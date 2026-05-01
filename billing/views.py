from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Billing
from .forms import BillingForm, UserEditForm


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

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('index')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'billing/edit_profile.html', {'form': form})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   # keep the user logged in
            messages.success(request, 'Password changed successfully.')
            return redirect('edit_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'billing/change_password.html', {'form': form})