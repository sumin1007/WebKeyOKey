from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views
from .forms import UserForm
from main.models import CustomUser

from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        find_u_id = request.POST['u_id']
        if form.is_valid():
            if CustomUser.objects.filter(u_id=find_u_id).exists():
                form = UserForm()
                return render(request, 'userapp/signup.html',{'form':form, 'error':'동일한 사업자번호가 존재합니다. 다른 번호를 입력해주세요'})
            if form.cleaned_data['password'] != form.cleaned_data['password_check']:
                form = UserForm()
                return render(request, 'userapp/signup.html',{'form':form, 'error':'비밀번호와 비밀번호 확인이 다릅니다.'})
            else:
                new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
                u_id=form.cleaned_data['u_id'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                question_id=form.cleaned_data['question_id'],
                answer=form.cleaned_data['answer'])

                login(request, new_user)
                return redirect('boss')
        else:
            return render(request, 'userapp/signup.html',{'form':form, 'error':'동일한 사업자번호가 존재합니다. 다른 번호를 입력해주세요'})
    else:
        form = UserForm()
        return render(request, 'userapp/signup.html', {'form': form})

def findpassword(request):
    if request.method == "POST":
        find_u_id = request.POST['u_id']
        username = request.POST['username']
        phone = request.POST['phone']
        answer = request.POST['answer']       
        if CustomUser.objects.filter(u_id=find_u_id).exists():
            user = get_object_or_404(CustomUser, u_id=find_u_id)
            if user.username == username and user.phone == phone and user.answer == answer:
                return redirect('password_reset')
        else:
            return redirect('findpassword')
    return render(request, 'userapp/findpassword.html')
