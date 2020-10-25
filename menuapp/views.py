from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from main.models import CustomUser, Menu, Option, Basket, Pay, Order
from datetime import datetime
from django.utils.dateformat import DateFormat
import random

# Create your views here.
def menu(request):
    menus = Menu.objects.all()
    user = request.user     #현재 로그인한 유저
    return render(request, 'menuapp/menu.html', {'menus':menus})

def optionmenu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    basket = Basket()
    if request.method == 'POST':
        basket.menu_id = menu
        basket.takeout = False
        if request.POST.getlist('takeout') != []:
            basket.takeout = True
        basket.count = request.POST['count']
        if int(basket.count) <= 0:  #수량을 음수로 선택했을 경우 다시 선택하도록 함
            return HttpResponse("수량을 다시 선택해주세요.")
        basket.ototal_price = menu.m_price
        check_values = request.POST.getlist('option[]')
        op_list = list()
        for c in check_values:
            if Option.objects.filter(option_name=c).exists():
                op = Option.objects.get(option_name=c)
                basket.ototal_price += op.option_price
                op_list.append(op)

        basket.ototal_price *= int(basket.count)
        basket.save()
        basket.b_options.add(*op_list)
    return render(request, 'menuapp/optionmenu.html', {'menu':menu})

def checkmenu(request):
    baskets = Basket.objects.all()
    money = 0
    for b in baskets:
        money +=  int(b.ototal_price)
    return render(request, 'menuapp/checkmenu.html', {'baskets': baskets, 'money':money})

def delete_basket(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return redirect('checkmenu')

def pay(request):
    money = 0
    for b in Basket.objects.all():
        money += int(b.ototal_price)
    if money == 0:
        return HttpResponse("주문금액이 0원입니다. 메뉴를 추가해주세요.")
    return render(request, 'menuapp/pay.html', {'money':money})

def success(request):
    pay = Pay()
    pay.user = request.user
    pay.date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    pay.total = 0
    pay.order_num = random.randrange(0,500)
    bt_list = list()
    or_list = list()
    for b in Basket.objects.all():
        pay.total += int(b.ototal_price)
        order = Order()
        order.or_name = b.menu_id.m_name
        order.or_num = pay.order_num
        order.or_count = b.count
        order.or_takeout = b.takeout
        for bt in b.b_options.all():
            bt_list.append(bt)
            
        order.save()
        order.or_options.add(*bt_list)
        bt_list.clear()
        or_list.append(order)
        
    pay.save()
    pay.orders.add(*or_list)
    
    for b in Basket.objects.all():
        b.delete()
    return render(request, 'menuapp/success.html', {'pay':pay})

def order(request):
    por_list = Pay.objects.all()
    return render(request, 'menuapp/order.html', {'por_list':por_list})

def delete_order(request, pk):
    # 한 고객의 모든 주문을 한번에 삭제
    pay = get_object_or_404(Pay, pk=pk)
    for o in pay.orders.all():
        o.delete()
    return redirect('order')

def orderdetail(request, pk):
    p_or = get_object_or_404(Pay, pk=pk)
    return render(request, 'menuapp/orderdetail.html', {'p_or':p_or})