from .models import *
from django.forms import ModelForm, HiddenInput, CharField, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ("name", "description", "price", "image", "category", "tags")
        
class BasketGoodsForm(ModelForm):
    
    class Meta:
        model = BasketGoods
        fields = ("client", "good", "amount", "discount")
        widgets = {
            'good': HiddenInput(),
            'client': HiddenInput(),
            'discount': HiddenInput(),
        }

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("deliveryAddress", "client")
        widgets = {
            "client": HiddenInput(),
        }

        
class ProfileForm(ModelForm):
    
    class Meta:
        model = Client
        fields = ("login", "password", "salt", "firstName", "lastName", "email")
        widgets = {
            'salt': HiddenInput(),
        }

class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = ("name", "description")

class TagForm(ModelForm):
    
    class Meta:
        model = Tag
        fields = ("name", "description")

class RegistrationForm(UserCreationForm):
    username = CharField(
        label = "User login",
        widget = TextInput(attrs={"class":"form-control", }),
        min_length=5
    )
    
    first_name = CharField(
        label="First name",
        widget = TextInput(attrs={"class":"form-control", }),
        max_length=255
    )
    
    last_name = CharField(
        label="Last name",
        widget = TextInput(attrs={"class":"form-control", }),
        max_length=255
    )
    
    email = CharField(
        label = "Email address",
        widget = EmailInput(attrs={"class":"form-control", }),
    )
    
    password1 = CharField(
        label = "Password",
        widget=PasswordInput(attrs={"class":"form-control", })
    )
    
    password2 = CharField(
        label = "Повторите пароль",
        widget=PasswordInput(attrs={"class":"form-control", })
    )
    
    class Meta:
        model=User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    
class LoginForm(AuthenticationForm):
    username = CharField(
        label = "User login",
        widget = TextInput(attrs={"class":"form-control", }),
        min_length=5
    )
    
    password1 = CharField(
        label = "Password",
        widget=PasswordInput(attrs={"class":"form-control", })
    )