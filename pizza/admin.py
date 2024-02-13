from django.contrib import admin
from .models import User, Pizza

# Register your models here.

admin.site.register(User)
admin.site.register(Pizza)