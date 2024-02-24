from django.contrib import admin
from .models import User, Pizza, Sauce, Cheese, Size, Order, CardExpiry

# Register your models here.

admin.site.register(User)
admin.site.register(Pizza)
admin.site.register(Sauce)
admin.site.register(Cheese)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(CardExpiry)