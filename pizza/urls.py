from .views import *
from django.urls import path

urlpatterns = [
 path('register/', UserSignupView.as_view(), name='register'),
 path('index/', index, name='index'),
 path('login/', LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
 path('logout/', logout_user, name="logout"),
 path('', welcome, name="welcome"),
 path('create_pizza/', create_pizza, name="create_pizza"),
 path('delivery/<int:pizza_id>/', delivery, name="delivery"),
 path('order/<int:order_id>/', order, name="order"),
 path('previous_order/<int:order_id>/', previous_order, name="previous_order"),
]
