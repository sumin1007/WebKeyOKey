from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import SigninForm

#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def home(request):
    signin_form = SigninForm()
    return render(request, 'main/home.html', {'signin_form': signin_form})

def signin(request):
    if request.method == "POST":
        u_id = request.POST['u_id']
        password = request.POST['password']
        user = authenticate(u_id = u_id, password = password)

        if user is not None:
            login(request, user)
            return redirect('boss')
        else:
            messages.error(request,'회원정보가 일치하지 않습니다. 다시 시도해주세요.')
            return redirect('home')

def boss(request):
    return render(request, 'main/boss.html')