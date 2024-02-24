# forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField, ValidationError
from .models import CardExpiry, Pizza, User, Order
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.forms import SelectDateWidget
from datetime import date, datetime


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'New Password'
        self.fields['password2'].label = 'Confirm New Password'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['crust', 'sauce', 'cheese', 'size', 'pepperoni', 'chicken', 'ham', 
                  'pineapple', 'peppers', 'mushrooms', 'onions']

class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'placeholder': _('Month'), 'class': 'input'}),
            forms.TextInput(attrs={'placeholder': _('Year'), 'class': 'input'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

class MonthYearField(forms.MultiValueField):
    widget = MonthYearWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(widget=forms.HiddenInput()),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            month, year = data_list
            return f'{year:04d}-{month:02d}'
        return None

class OrderForm(forms.ModelForm):

    expiry = MonthYearField(label=_('Expiry Date'))
    class Meta:
        model = Order
        fields = ['name', 'address', 'card_number', 'expiry', 'cvv']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.TextInput(attrs={'class': 'input'}),
            'card_number': forms.TextInput(attrs={'class': 'input'}),
            'cvv': forms.TextInput(attrs={'class': 'input'}),
        }

        

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        return card_number

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry')

        if expiry:
            try:
                year, month = map(int, expiry.split('-'))
                current_year = date.today().year
                current_month = date.today().month

                if not (1 <= month <= 12):
                    raise ValidationError(_('Invalid month. Please enter a value between 1 and 12.'))

                if not (current_year <= year <= current_year + 20):
                    raise ValidationError(_('Invalid year. Please enter a value within the next 20 years.'))

                if year == current_year and month < current_month:
                    raise ValidationError(_('The expiry date has already passed.'))

                # Create a CardExpiry instance
                expiry_instance, _ = CardExpiry.objects.get_or_create(year=year, month=month)


            except ValueError:
                raise ValidationError(_('Invalid expiry date format. Use YYYY-MM.'))

            return expiry_instance



    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        return cvv