from .views import *
from django.urls import path

urlpatterns = [
 path('', UserSignupView.as_view(), name='register'),
 path('index/', index, name='index'),
 path('login/', LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
 path('logout/', logout_user, name="logout"),
]
