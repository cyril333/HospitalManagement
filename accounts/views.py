from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
    return render(request, 'login.html')

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')