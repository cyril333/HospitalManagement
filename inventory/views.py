from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import InventoryMedicine, Supplies
from .forms import InventoryMedicineForm, SuppliesForm

# --- MEDICINE VIEWS ---


@login_required(login_url='/login/')
def inventory_home(request):
    medicine_count = InventoryMedicine.objects.count()
    supplies_count = Supplies.objects.count()
    return render(request, 'inventory/index.html', {   
        'medicine_count': medicine_count,
        'supplies_count': supplies_count,
    })

@login_required(login_url='/login/')
def medicine_list(request):
    medicines = InventoryMedicine.objects.all()
    return render(request, 'inventory/medicine_list.html', {'medicines': medicines})

@login_required(login_url='/login/')
def medicine_add(request):
    form = InventoryMedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('medicine_list')
    return render(request, 'inventory/addNewInventoryMedicine.html', {'form': form})

@login_required(login_url='/login/')
def medicine_edit(request, pk):
    medicine = get_object_or_404(InventoryMedicine, pk=pk)
    form = InventoryMedicineForm(request.POST or None, instance=medicine)
    if form.is_valid():
        form.save()
        return redirect('medicine_list')
    return render(request, 'inventory/medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

@login_required(login_url='/login/')
def medicine_delete(request, pk):
    medicine = get_object_or_404(InventoryMedicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'inventory/confirm_delete.html', {'item': medicine.medicine_name})


# --- SUPPLIES VIEWS ---

@login_required(login_url='/login/')
def supplies_list(request):
    supplies = Supplies.objects.all()
    return render(request, 'inventory/supplies_list.html', {'supplies': supplies})

@login_required(login_url='/login/')
def supplies_add(request):
    form = SuppliesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('supplies_list')
    return render(request, 'inventory/supplies_form.html', {'form': form, 'title': 'Add Supply'})

@login_required(login_url='/login/')
def supplies_edit(request, pk):
    supply = get_object_or_404(Supplies, pk=pk)
    form = SuppliesForm(request.POST or None, instance=supply)
    if form.is_valid():
        form.save()
        return redirect('supplies_list')
    return render(request, 'inventory/supplies_form.html', {'form': form, 'title': 'Edit Supply'})

@login_required(login_url='/login/')
def supplies_delete(request, pk):
    supply = get_object_or_404(Supplies, pk=pk)
    if request.method == 'POST':
        supply.delete()
        return redirect('supplies_list')
    return render(request, 'inventory/confirm_delete.html', {'item': supply.supply_name})