from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate

from core.models import * 


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
                if user.user_type == '3':
                    return redirect('provider-home') 
                else:
                    return redirect('index')
            else:
                return render(request, 'core/login.html', {'message': 'Password không đúng!!'}, status=401)
        except Exception as e:
            return render(request, 'core/login.html', {'message': f'User với {username} không tồn tại!'}, status=500)
    return render(request, 'core/login.html', status=200)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')
