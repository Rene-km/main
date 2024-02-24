# models.py

from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime 
from datetime import date
#... any other imports

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()



Crust = [
    ('REGULAR', 'Regular'),
    ('THIN', 'Thin'),
]



  
class Sauce(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


 

class Cheese(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Size(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.DecimalField(max_digits=4, decimal_places=2, default=7)

    def __str__(self) -> str:
        return str(self.size)


class Pizza(models.Model):
   
   
   id = models.AutoField(primary_key=True)
   pepperoni = models.BooleanField( verbose_name=('Pepperoni'), default=False)
   chicken = models.BooleanField(verbose_name=('Chicken'), default=False,)
   ham = models.BooleanField(verbose_name=('Ham'), default=False)
   pineapple = models.BooleanField(verbose_name=('Pineapple'), default=False)
   peppers = models.BooleanField(verbose_name=('Peppers'), default=False)
   mushrooms = models.BooleanField(verbose_name=('Mushrooms'), default=False)
   onions = models.BooleanField(verbose_name=('Onions'), default=False)
   crust = models.CharField(max_length=50, choices=Crust, default='REGULAR')
   sauce = models.ForeignKey(Sauce, null=True ,on_delete = models.CASCADE)
   cheese = models.ForeignKey(Cheese, null=True ,on_delete = models.CASCADE)
   size = models.ForeignKey(Size,null=True ,on_delete = models.CASCADE)

   def __str__(self) -> str:
        return f"{self.size} {self.crust} Pizza"
   
   def get_selected_toppings(self):
       selected_toppings= []
       if self.pepperoni == True:
           selected_toppings.append('Pepperoni')
       if self.chicken == True:
           selected_toppings.append('Chicken')
       if self.ham == True:
           selected_toppings.append('Ham')
       if self.pineapple == True:
           selected_toppings.append('Pineapple')
       if self.peppers == True:
           selected_toppings.append('Peppers')
       if self.mushrooms == True:
           selected_toppings.append('Mushrooms')
       if self.onions == True:
           selected_toppings.append('Onions')
       return selected_toppings
   
   def get_total_price(self):
       base_price = 8
       toppings_price = 1
       total_price = 0

       if self.size.size == 7:
           total_price += base_price
       if self.size.size == 9.50:
           total_price += base_price + 2
       if self.size.size == 11.5:
           total_price += base_price + 4
       if self.size.size == 13.5:
           total_price += base_price + 6

       total_price = total_price + (len(self.get_selected_toppings()) * toppings_price)
       return total_price
           

       
   
   
   


def validate_length(value):
    if len(str(value)) < 16 or len(str(value)) > 16 :
        raise ValidationError(
            _("Value entered must be 16 digits"),
            params={"value": value},
        )
    
def validate_cvv(value):
    if len(str(value)) < 3 or len(str(value)) > 3 :
        raise ValidationError(
            _("Value entered must be 3 digits"),
            params={"value": value},
        )





class CardExpiry(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField()
    year = models.IntegerField()



    def __str__(self):
        return f"{self.month}/{self.year}"
    
    def clean(self):
        current_year = date.today().year
        current_month = date.today().month

        if not (1 <= self.month <= 12):
            raise ValidationError("Month must be a number between 1 and 12.")
        
        if len(str(self.year)) < 4:
            raise ValidationError("Year must be at least 4 digits.")
        
        if self.year > current_year + 20:
            raise ValidationError("Year cannot be more than 20 years in the future.")

        if self.year < current_year or (self.year == current_year and self.month < current_month):
            raise ValidationError("Card has expired.")
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    pizza = models.ForeignKey(Pizza,null=True, on_delete=models.CASCADE)
    address = models.TextField(max_length=150,default="Dublin")
    card_number = models.PositiveBigIntegerField(default=0000000000000000, validators=[validate_length])
    expiry = models.ForeignKey(CardExpiry, on_delete=models.CASCADE)
    cvv = models.IntegerField(default=000, validators=[validate_cvv])
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)

    
