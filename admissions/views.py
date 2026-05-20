from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Admission, AdmissionSupplyUsage
from .forms import AdmissionForm, AdmissionSupplyUsageForm

@login_required(login_url='/login/')
def admission_list(request):
    admissions = Admission.objects.all()
    return render(request, 'admissions/admission_list.html', {'admissions': admissions})

@login_required(login_url='/login/')
def admission_add(request):
    form = AdmissionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admission_list')
    return render(request, 'admissions/form.html', {'form': form, 'title': 'Add Admission', 'back_url': 'admission_list'})

@login_required(login_url='/login/')
def admission_edit(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    form = AdmissionForm(request.POST or None, instance=admission)
    if form.is_valid():
        form.save()
        return redirect('admission_list')
    return render(request, 'admissions/form.html', {'form': form, 'title': 'Edit Admission', 'back_url': 'admission_list'})

@login_required(login_url='/login/')
def admission_delete(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        admission.delete()
        return redirect('admission_list')
    return render(request, 'admissions/confirm_delete.html', {'item': f"Admission #{admission.admission_id}"})