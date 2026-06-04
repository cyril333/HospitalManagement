from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.views import admin_required
from .models import InventoryMedicine, Supplies
from .forms import InventoryMedicineForm, SuppliesForm


@admin_required
def inventory_home(request):
    medicines = InventoryMedicine.objects.all()
    supplies = Supplies.objects.all()

    context = {
        'medicine_count': medicines.count(),
        'supplies_count': supplies.count(),
        'low_medicine_count': medicines.filter(quantity__lt=10, quantity__gt=0).count(),
        'out_medicine_count': medicines.filter(quantity__lte=0).count(),
        'low_supply_count': supplies.filter(quantity__lt=10, quantity__gt=0).count(),
        'out_supply_count': supplies.filter(quantity__lte=0).count(),
    }
    return render(request, 'inventory/inventory_home.html', context)


@admin_required
def medicine_list(request):
    medicines = InventoryMedicine.objects.all()

    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    stock = request.GET.get('stock', '').strip()

    if search:
        medicines = medicines.filter(medicine_name__icontains=search)
    if category:
        medicines = medicines.filter(category=category)
    if stock == 'low':
        medicines = medicines.filter(quantity__lt=10, quantity__gt=0)
    elif stock == 'out':
        medicines = medicines.filter(quantity__lte=0)
    elif stock == 'ok':
        medicines = medicines.filter(quantity__gte=10)

    categories = InventoryMedicine.objects.values_list('category', flat=True).distinct().order_by('category')

    return render(request, 'inventory/medicine_list.html', {
        'medicines': medicines,
        'categories': categories,
        'selected_search': search,
        'selected_category': category,
        'selected_stock': stock,
    })


@admin_required
def medicine_add(request):
    form = InventoryMedicineForm(request.POST or None)
    if form.is_valid():
        medicine = form.save()
        messages.success(request, f'Medicine "{medicine.medicine_name}" added successfully.')
        return redirect('medicine_list')
    return render(request, 'inventory/medicine_form.html', {
        'form': form,
        'title': 'Add New Medicine',
        'subtitle': 'Create a medicine inventory record with validated stock and pricing details.',
        'back_url': 'medicine_list'
    })


@admin_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(InventoryMedicine, pk=pk)
    form = InventoryMedicineForm(request.POST or None, instance=medicine)
    if form.is_valid():
        medicine = form.save()
        messages.success(request, f'Medicine "{medicine.medicine_name}" updated successfully.')
        return redirect('medicine_list')
    return render(request, 'inventory/medicine_form.html', {
        'form': form,
        'title': 'Edit Medicine',
        'subtitle': 'Update medicine information, stock, unit, and price.',
        'back_url': 'medicine_list'
    })


@admin_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(InventoryMedicine, pk=pk)
    if request.method == 'POST':
        name = medicine.medicine_name
        medicine.delete()
        messages.success(request, f'Medicine "{name}" deleted successfully.')
        return redirect('medicine_list')
    return render(request, 'inventory/confirm_delete.html', {'item': medicine.medicine_name})


@admin_required
def supplies_list(request):
    supplies = Supplies.objects.all()

    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    stock = request.GET.get('stock', '').strip()

    if search:
        supplies = supplies.filter(supply_name__icontains=search)
    if category:
        supplies = supplies.filter(category=category)
    if stock == 'low':
        supplies = supplies.filter(quantity__lt=10, quantity__gt=0)
    elif stock == 'out':
        supplies = supplies.filter(quantity__lte=0)
    elif stock == 'ok':
        supplies = supplies.filter(quantity__gte=10)

    categories = Supplies.objects.values_list('category', flat=True).distinct().order_by('category')

    return render(request, 'inventory/supplies_list.html', {
        'supplies': supplies,
        'categories': categories,
        'selected_search': search,
        'selected_category': category,
        'selected_stock': stock,
    })


@admin_required
def supplies_add(request):
    form = SuppliesForm(request.POST or None)
    if form.is_valid():
        supply = form.save()
        messages.success(request, f'Supply "{supply.supply_name}" added successfully.')
        return redirect('supplies_list')
    return render(request, 'inventory/supplies_form.html', {
        'form': form,
        'title': 'Add New Supply',
        'subtitle': 'Create a supply inventory record with validated stock and pricing details.',
        'back_url': 'supplies_list'
    })


@admin_required
def supplies_edit(request, pk):
    supply = get_object_or_404(Supplies, pk=pk)
    form = SuppliesForm(request.POST or None, instance=supply)
    if form.is_valid():
        supply = form.save()
        messages.success(request, f'Supply "{supply.supply_name}" updated successfully.')
        return redirect('supplies_list')
    return render(request, 'inventory/supplies_form.html', {
        'form': form,
        'title': 'Edit Supply',
        'subtitle': 'Update supply information, stock, unit, and price.',
        'back_url': 'supplies_list'
    })


@admin_required
def supplies_delete(request, pk):
    supply = get_object_or_404(Supplies, pk=pk)
    if request.method == 'POST':
        name = supply.supply_name
        supply.delete()
        messages.success(request, f'Supply "{name}" deleted successfully.')
        return redirect('supplies_list')
    return render(request, 'inventory/confirm_delete.html', {'item': supply.supply_name})