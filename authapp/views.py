from django.shortcuts import render, redirect
from authapp.forms import SignUpForm
from authapp.forms import LoginForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['username'] = request.POST.get('email')
        form = SignUpForm(data)

        if form.is_valid():
            email = form.cleaned_data['email']
            form.cleaned_data['username'] = email
            user = form.save()
            return JsonResponse({'success': True}) 
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,'errors':{'Xəta':["Yanlış ad və ya şifrə"]}})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')