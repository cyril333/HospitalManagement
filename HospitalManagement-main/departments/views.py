from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Department, Room
from .forms import DepartmentForm, RoomForm

@login_required(login_url='/login/')
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required(login_url='/login/')
def department_add(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    return render(request, 'departments/form.html', {'form': form, 'title': 'Add Department', 'back_url': 'department_list'})

@login_required(login_url='/login/')
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    return render(request, 'departments/form.html', {'form': form, 'title': 'Edit Department', 'back_url': 'department_list'})

@login_required(login_url='/login/')
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('department_list')
    return render(request, 'departments/confirm_delete.html', {'item': dept.department_name})

@login_required(login_url='/login/')
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'departments/room_list.html', {'rooms': rooms})

@login_required(login_url='/login/')
def room_add(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'departments/form.html', {'form': form, 'title': 'Add Room', 'back_url': 'room_list'})

@login_required(login_url='/login/')
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'departments/form.html', {'form': form, 'title': 'Edit Room', 'back_url': 'room_list'})

@login_required(login_url='/login/')
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'departments/confirm_delete.html', {'item': room.room_number})