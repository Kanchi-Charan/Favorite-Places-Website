from importlib.resources import contents
from xml.etree.ElementInclude import include
from django import forms
from .models import FavoritePlace


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,min_length = 5,label="User Name",required=True,error_messages={
        "required":"User Name must required to register.",
        "max_length":"Lenth of the user name should not be greater than 100.",
        "min_length":"Length of the user name should not be smaller than 5."
    })
    first_name = forms.CharField(max_length=100,required=True,label="First Name",error_messages={
        "required":"First Name must required",
        "max_length":"First Name must not be greater then 100 characters",
    })
    last_name = forms.CharField(max_length=100,label="Last Name",required=True,error_messages={
        "required":"Last Name must required",
        "max_length":"Last Name must not be greater then 100 characters",
    })
    email = forms.EmailField(label = "Email Id",required=True)
    password = forms.CharField(label= "Enter Password",max_length=32)
    password1 = forms.CharField(label = "Renter Password",max_length=32)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,label="User Name",required=True,error_messages={
        "required":"User Name must NOT empty.",
        "max_length":"User Name cannot be more than 100 characters."
    })

    password = forms.CharField(max_length=30,required=True,label="Password",error_messages={
        "required":"Please enter your password to login.",
    })


class PostsForm(forms.Form):
    place_name = forms.CharField(max_length=150,label = "Place Name")
    slug = forms.SlugField()
    address = forms.CharField(max_length=200,label = "Address")
    image = forms.ImageField(label="Upload Image")
    content = forms.CharField(min_length=10,label="Describe about Place",widget=forms.Textarea)


class CommentsForm(forms.Form):
    comment = forms.CharField(label = "Comment",widget = forms.Textarea)