from django import forms
from django_countries.fields import CountryField # Library for countries
from phonenumber_field.formfields import PhoneNumberField # Library for phone numbers
from . import models

# Comments in classes mean that a package needs to be installed to create a field for that class

# Note: The Manage Site Form is not included here.

# Customer sign up form

class CustomerSignupForm(forms.Form):

    firstName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'First Name'}), label='First Name', max_length=64)
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name'}), label='Last Name', max_length=64)
    userName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}), label='Choose Username', max_length=64)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'name@example.com'}), label='Email Address', max_length=64)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control mb-3', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}), label='Birthday')
    streetAddress = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '99 Example Street'}), label='Address', max_length=64)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'City/Town'}), label='City/Town', max_length=64)
    suburb = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Suburb'}), label='Suburb', max_length=64)
    postalCode = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Postal Code'}), label='Postal Code')
    country = CountryField().formfield(widget=forms.Select(attrs={'class': 'form-control mb-3', 'placeholder': 'Country'}), label='Country')
    phoneNumber = PhoneNumberField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Phone Number (e.g. +XX 12 345 6789)'}), max_length=20, label='Phone Number')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}), label='Password', max_length=16)
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password'}), label='Confirm Password', max_length=16)

# Business sign up form

class BusinessSignupForm(forms.Form):

    businessName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Business Name'}), label='Business Name', max_length=128)
    userName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Business Username'}), label='Choose Business Username', max_length=64)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email Address'}), label='Email Address', max_length=64)
    streetAddress = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '99 Example Street'}), label='Address', max_length=64)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'City/Town'}), label='City/Town', max_length=64)
    suburb = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Suburb'}), label='Suburb', max_length=64)
    postalCode = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Postal Code'}), label='Postal Code')
    country = CountryField().formfield(widget=forms.Select(attrs={'class': 'form-control mb-3', 'placeholder': 'Country'}), label='Country')
    contactNumber = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Contact Number (e.g. +XX 12 345 6789)'}), label='Contact Number', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}), label='Password', max_length=16)
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password'}), label='Confirm Password', max_length=16)


# Customer login form
class CustomerLoginForm(forms.Form):
    userName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}), label='Username', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}), label='Password', max_length=64)

# Business login form

class BusinessLoginForm(forms.Form):
    userName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Business Username'}), label='Business Username', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}), label='Password', max_length=64)

class ProductRegistrationForm(forms.Form):
    productName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Product Name'}), label='Product Name', max_length=64)
    productDepartment = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control mb-3', 'placeholder': 'Product Name'}, choices=models.ProductDepartment.objects.all().values_list('id', 'departmentName')), label='Product Department')
    productPrice = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Price (in Rands)'}), label='Set Price')
    productInformation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Product Information'}), label='Product Information')
    productImage = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control mb-3'}), label='Product Image')