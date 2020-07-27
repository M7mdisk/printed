from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, Http404,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import *
import json
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = request.POST
        print("***************************", form['shop'])
        shop = Shop.objects.filter(name=form['shop']).first()
        return redirect(f'/order/{shop.id}/')
    else:
        if request.user.is_authenticated :
            shopslist = Shop.objects.all()
            data = serializers.serialize('json', shopslist)
            print(shopslist)
            context = {'shops': data}
            if request.user.profile.isOwner:
                shopslist = Shop.objects.filter(owner =request.user.profile)
                context = {'shops': shopslist}
                return render(request, 'shops/indexowner.html', context)
            return render(request, 'shops/index.html', context)
        else:
            return render(request, 'shops/index1.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! logging you in')
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = UserRegisterForm()
    return render(request, 'shops/register.html', {'form': form})

def registerOwner(request):
    if request.method == 'POST':
        form = OwnerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/')
    else:
        form = OwnerCreateForm({'isOwner':True})
    return render(request, 'shops/registerowner.html', {'form': form})

@login_required(login_url='/login/')
def create_order(request, pk):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            messages.success(request, f'Order Number {a} placed!. Total price is {a.total}')
            return redirect('/')
    else:
        form = PlaceOrderForm({'shop': Shop.objects.filter(id=pk).first(),'buyer' :request.user.profile})
        shopp = Shop.objects.filter(id=pk).first()
        if shopp == None:
            raise Http404("Shop not found")   
        return render(request, 'shops/order.html', {'form': form,'shopp':shopp,})

@login_required(login_url='/login/')
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user.profile)
    context = {
        'orders': orders,
    }
    return render(request, "shops/dashcustomer.html", context)

@login_required(login_url='/login/')
def create_shop(request):
    if not request.user.profile.isOwner:
        raise PermissionDenied()
    if request.method == 'POST':
        form = CreateShopForm(request.POST)
        if form.is_valid():
            a = form.save()
            messages.success(request, f'Shop {a} Created!')
            return redirect('/')
    else:
        form = CreateShopForm({'owner': request.user.profile})  
    return render(request, 'shops/newshop.html', {'form': form,})


# @login_required(login_url='/login/')
# def dash(request):
#     if request.method == 'POST':
#         order = Order.objects.filter(uuid=request.POST.get('order')).first()
#         order.status = request.POST.get('status')
#         order.save() 
#     shopu = Shop.objects.filter(owner=request.user.profile)
#     orders = Order.objects.filter(shop__in=shopu)
#     context = {
#         'orders': orders,
#     }
#     return render(request, "shops/dash.html", context)

# @login_required(login_url='/login/')
# def dash_shop(request,pk):
#     shopu = Shop.objects.filter(id=pk).first()
#     if shopu == None:
#         raise Http404("Shop not found")
#     if not shopu.owner == request.user.profile:
#         raise HttpResponseForbidden("You don't own shop")

#     orders_list = Order.objects.filter(shop=shopu)
#     paginator = Paginator(orders_list,1)
#     page = request.GET.get('page')
#     orders = paginator.get_page(page)
#     context = {
#         'orders': orders,
#     }
#     return render(request, "shops/dash.html", context)
class OrdersList(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 1
    template_name='shops/dash.html'
    def get_queryset(self):
        print("-----------------------------",self.kwargs.get("pk"))
        if self.kwargs.get("pk") is None:
            shopu = Shop.objects.filter(owner=self.request.user.profile)
            return Order.objects.filter(shop__in=shopu)
        else:
            pk = self.kwargs.get("pk")
            shopu = Shop.objects.filter(id=pk).first()
            return Order.objects.filter(shop=shopu)           


def about(request):
    return render(request,"shops/about.html")

def delete_shop(request,pk):
    shop = Shop.objects.filter(id=pk)