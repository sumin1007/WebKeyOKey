from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from main.models import Menu, Option, CustomUser, Pay
from .forms import AddForm, EditForm, OptionForm, CustomForm
from datetime import datetime
from django.utils.dateformat import DateFormat

def setting(request):
    return render(request, 'settingapp/setting.html') 

def settingmenu(request):
    menus = Menu.objects.all()
    user = request.user
    return render(request, 'settingapp/settingmenu.html', {'menus': menus})

def addmenu(request):
    options = Option.objects.all()
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user
            form.save()
            return redirect('settingmenu')
    else:
        form = AddForm()
        return render(request, 'settingapp/addmenu.html', {'form':form, 'options':options})

def editmenu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = EditForm(request.POST, instance=menu)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('settingmenu')
    else:
        form = EditForm(instance=menu)
        return render(request, 'settingapp/editmenu.html', {'form':form})

def delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    return redirect('settingmenu')

def optionlist(request):
    return render(request, 'settingapp/optionlist.html')

def bye(request):
    return render(request, 'settingapp/bye.html')

def option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('addmenu')
    else:
        form = OptionForm()
        return render(request, 'settingapp/option.html', {'form':form})

def delete_option(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    # post.delete()
    option = get_object_or_404(Option, pk=pk)
    option.delete()
    return redirect('settingmenu')

def delete_user(request):
    request.user.delete()
    return redirect('home')

# 달력구현
import datetime
import calendar
from .calendar import Calendar
from django.utils.safestring import mark_safe

def sales(request):
    today = get_date(request.GET.get('month'))

    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(withyear=True)
    result_cal = mark_safe(html_cal)

    user = request.user
    pays = Pay.objects.filter(user=user)
    pyear = 0
    pmonth = 0
    pday = 0
    for pay in pays:
        if pay.date.year == today.year:
            pyear += pay.total
        if pay.date.month == today.month:
            pmonth += pay.total
        if pay.date.day == today.day:
            pday += pay.total

    context = {'calendar' : result_cal, 'prev_month' : prev_month_var, 'next_month' : next_month_var, 'pyear':pyear, 'pmonth':pmonth, 'pday':pday }

    return render(request, 'settingapp/sales.html', context)

#현재 달력을 보고 있는 시점의 시간을 반환
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

#현재 달력의 이전 달 URL 반환
def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

#현재 달력의 다음 달 URL 반환
def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
