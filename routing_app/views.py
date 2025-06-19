from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.utils.decorators import method_decorator

from .models import *
from .forms import *
import hashlib
import uuid
import base64

# users
def index(request):
    return render(request, 'users/home.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if(form.is_valid()):
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "users/signin.html", context)

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if(form.is_valid()):
            
            client = Client()
            client.login = form.data['username']
            client.firstName = form.data['first_name']
            client.lastName = form.data['last_name']
            client.email = form.data['email']
            
            salt = str(uuid.uuid4())[:32]
            salted_password = salt.encode('utf-8') + form.data['password1'].encode('utf-8')
            password = base64.b64encode(hashlib.sha256(salted_password).digest()).decode('utf-8')
            client.password = password
            client.salt = salt
            
            client.save()
            
            login(request, form.save())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
    else:
        form = RegistrationForm()
    context = {
        "form": form
    }
    return render(request, "users/signup.html", context)

@login_required 
def logout_user(request):
    logout(request)
    return redirect("/")
    
@login_required
def profile(request):
    
    data = get_object_or_404(Client, login=request.user.username)
    
    if request.method == 'POST':
        form = request.POST.copy()
        salt = str(uuid.uuid4())[:32]
        
        request.user.set_password(form['password'])
        request.user.save()
        
        salted_password = salt.encode('utf-8') + form['password'].encode('utf-8')
        password = base64.b64encode(hashlib.sha256(salted_password).digest()).decode('utf-8')
        
        form['password']=password
        form['salt']=salt
        profileForm = ProfileForm(form, instance=data)
        profileForm.save()
        context = { "form": profileForm }
        return redirect("/profile/")
    else:
        data.password = ''
        profile = ProfileForm(instance = data)
        context = { "form": profile }
        return render(request, 'routing_practice/profile.html', context)



# Catalogue root
def catalogue_details(request, pk):
    good = Goods.objects.get(pk=pk)
    
    if good is None:
        return HttpResponse("Error!", status=404, reason=f"Good {pk} not found in db")
    
    if request.method == 'POST':
        user = get_object_or_404(Client, login=request.user.username)
        
        form = BasketGoodsForm(data=request.POST)
        
        basketGoods = BasketGoods()
        basketGoods.client = user
        basketGoods.good = good
        basketGoods.amount = form.data["amount"]
        basketGoods.save()
        
        return redirect("/basket/")
    else:
        context = {
            "item": good,
            "basket_form": BasketGoodsForm()
        }
        return render(request, "routing_practice/catalogue_detail.html", context)

class CatalogueCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "routing_app.add_goods"
    model = Goods
    form_class = GoodsForm
    template_name = "routing_practice/catalogue_insert.html"
    success_url = reverse_lazy('catalogue_list')

class CatalogueUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "routing_app.change_goods"
    model = Goods
    form_class = GoodsForm
    template_name = "routing_practice/catalogue_insert.html"
    success_url = reverse_lazy('catalogue_list')

class CatalogueDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "routing_app.delete_goods"
    model = Goods
    template_name = "routing_practice/catalogue_confirm_delete.html"
    success_url = reverse_lazy('catalogue_list')
    context_object_name = 'item'

def catalogue(request):
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    if category is None and tag is None:
        data = Goods.objects.all()
    elif category is not None:
        if(tag is not None):
            data = Goods.objects.filter(category__name=category, tags__name=tag)
        else:
            data = Goods.objects.filter(category__name=category)
    else:
        data = Goods.objects.filter(tags__name=tag)
    context = { "list_items": data }
    return render(request, "routing_practice/catalogue.html", context)

@login_required 
def catalogue_feedback(request):
    if request.method == 'POST':
        data = request.POST
        return redirect('/catalogue')
    else:
        return render(request, 'routing_practice/catalogue_feedback.html')



# Basket root
@login_required
@permission_required("routing_app.view_basketgoods")
def basket(request):
    user = get_object_or_404(Client, login=request.user.username)
    
    items = BasketGoods.objects.filter(client__id=user.id)
    
    totalSum = 0
    for item in items:
        totalSum += item.good.price * item.amount
    
    context = { "list_items": items, "totalSum": totalSum }
    return render(request, 'basket/basket.html', context)

@login_required
@permission_required("routing_app.delete_basketgoods")
def basket_clear(request):
    user = get_object_or_404(Client, login=request.user.username)
    
    if(user is None):
        return HttpResponse("Error!", status=404, reason=f"User {request.user.username} not found in db")
    basket = BasketGoods.filter(client__id=user.id)
    
    if request.method == 'POST':
        basket.delete()
        return redirect("/")
    else:
        totalSum = 0
        for item in basket:
            totalSum += item.good.price * item.amount
        
        context = {
            "total_count": basket.count(),
            "total_sum": totalSum
        }
        return render(request, "basket/basket_confirm_clear.html", context)

@login_required
@permission_required("routing_app.add_order")
def create_order(request):
    user = get_object_or_404(Client, login=request.user.username)
    basket = BasketGoods.objects.filter(client__id=user.id)
    
    if(basket.count() <=0):
        return redirect("catalogue/")
    
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        
        order = Order()
        order.deliveryAddress = form.data["deliveryAddress"]
        order.client = user
        
        order.save()
        
        for item in basket:
            orderGood = OrderGoods()
            orderGood.order = order
            orderGood.good = item.good
            orderGood.amount = item.amount
            orderGood.discount = item.discount
            orderGood.save()
            
        basket.delete()
        return redirect("/")
    else:
        totalSum = 0
        for item in basket:
            totalSum += item.good.price * item.amount
        
        context = {
            "form": OrderForm(),
            "total_count": basket.count(),
            "total_sum": totalSum
        }
        return render(request, "basket/basket_confirm_order.html", context)

@method_decorator(login_required, "dispatch")
class BasketDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "routing_app.delete_basketgoods"
    model = BasketGoods
    template_name = "/basket/basket_confirm_delete.html"
    success_url = reverse_lazy("basket_page")
    context_object_name = 'item'

# Orders root
@login_required
@permission_required('routing_app.view_order')
def orders(request):
    if request.user.groups.filter(name='Byer').exists():
        orders=Order.objects.filter(client__login=request.user.username)
    else:
        orders=Order.objects.all()
    
    context = {
        "list_items": orders
    }
    return render(request, "orders/orders.html", context)

@login_required
@permission_required('routing_app.view_order')
def order_details(request, pk):
    order = Order.objects.get(pk=pk)
    order_goods = OrderGoods.objects.filter(order__id=order.id)
    
    totalSum = 0
    for orderGood in order_goods:
        totalSum += orderGood.good.price * orderGood.amount
    
    context = {
        "order": order,
        "order_goods": order_goods,
        "total_sum": totalSum
    }
    
    return render(request, "orders/order_details.html", context)

@method_decorator(login_required, "dispatch")
class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "routing_app.delete_order"
    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy('orders_page')
    context_object_name = 'item'
    
# Categories root
class CategoryListView(ListView):
    model = Category
    template_name = "category/categories.html"
    context_object_name = 'categories'

class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "routing_app.add_category"
    model = Category
    form_class = CategoryForm
    template_name = "category/category_insert.html"
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "routing_app.change_category"
    model = Category
    form_class = CategoryForm
    template_name = "category/category_insert.html"
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "routing_app.delete_category"
    model = Category
    template_name = "category/category_delete.html"
    success_url = reverse_lazy('category_list')
   
   
    
# Tags root
class TagListView(ListView):
    model = Tag
    template_name = "tag/tags.html"
    context_object_name = 'tags'
    
class TagCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "routing_app.add_tag"
    model = Tag
    form_class = TagForm
    template_name = "tag/tag_insert.html"
    success_url = reverse_lazy('tag_list')

class TagUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "routing_app.change_tag"
    model = Tag
    form_class = TagForm
    template_name = "tag/tag_insert.html"
    success_url = reverse_lazy('tag_list')

class TagDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "routing_app.delete_tag"
    model = Tag
    template_name = "tag/tag_delete.html"
    success_url = reverse_lazy('tag_list')
