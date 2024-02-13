# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

Toppings = [
    ('PEPPERONI', 'Pepperoni'),
    ('SWEETCORN', 'Sweetcorn'),
    ('MEATBALLS', 'Meatballs'),
]

Cheese = [
    ('MOZARELLA', 'Mozarella'),
    ('CHEDDER', 'Chedder'),
]


Crust = [
    ('REGULAR', 'Regular'),
    ('THIN', 'Thin'),
]

Size = [
    ('7', 'Personal'),
    ('9.5', 'Medium'),
]

  
class Sauce(models.Model):
    name = models.CharField(max_length=100)


class Pizza(models.Model):
   id = models.AutoField(primary_key=True)
   Pepperoni = models.BooleanField( verbose_name=('Pepperoni'), default=False)
   Chicken = models.BooleanField(verbose_name=('Chicken'), default=False,)
   Ham = models.BooleanField(verbose_name=('Ham'), default=False)
   Pineapple = models.BooleanField(verbose_name=('Pineapple'), default=False)
   Peppers = models.BooleanField(verbose_name=('Peppers'), default=False)
   Mushrooms = models.BooleanField(verbose_name=('Mushrooms'), default=False)
   Onions = models.BooleanField(verbose_name=('Onions'), default=False)
   size = models.CharField(max_length=50, choices=Size, default='7')
   crust = models.CharField(max_length=50, choices=Crust, default='REGULAR')
   cheese = models.CharField(max_length=50, choices=Cheese, default='MOZARELLA')
 
   # charfields have to have a max length

    
