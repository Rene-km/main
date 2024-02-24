import logging
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import * 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Order


class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index/')

@login_required
def index(request):
    current_user = request.user
    user_id = current_user.id
    orders = Order.objects.filter(user=current_user)
    return render(request, 'index.html', {'orders':orders})

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")


def welcome(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'welcome.html')

@login_required
def create_pizza(request):
    user = request.user

    if request.method == "POST":
        form = PizzaForm(request.POST)
        if form.is_valid():
            new_pizza = form.save()
            request.session['pizza_id'] = new_pizza.id
            return redirect('delivery', pizza_id=new_pizza.id)
        else:
            return render(request, 'create_pizza.html', {'form':form})
    else:
    #     # its a GET request
    #     # load a new instance of the BookForm 
    #     # show it to the user
        form = PizzaForm()
        return render(request, 'create_pizza.html', {'form': form})

@login_required
def delivery(request, pizza_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.pizza = Pizza.objects.get(id=pizza_id)
            order.save()
            return redirect('order', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'delivery.html', {'form': form})


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def previous_order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'previous_order.html', {'order': order})