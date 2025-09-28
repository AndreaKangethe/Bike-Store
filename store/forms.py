# forms.py

from django import forms
from .models import Bike, Review, Profile # Consolidated imports
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        # Add the widgets attribute here
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,  # Set the desired number of rows (height)
                'class': 'form-control' # Apply Bootstrap class
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control' # Apply Bootstrap class here too for consistency
            })
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        # Optional: Add widgets here if you want to apply form-control class directly
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['name', 'model', 'brand', 'price', 'engine_cc', 'available', 'image']
        labels = {
            'name': 'Bike Name',
            'model': 'Bike Model',
            'brand': 'Brand',
            'price': 'Price (Ksh)',
            'engine_cc': 'Engine CC',
            'available': 'Available for Sale',
            'image': 'Bike Image',
        }
        help_texts = {
            'price': 'Enter the price in Kenyan Shillings.',
            'engine_cc': 'Specify the engine displacement in cubic centimeters (cc).',
            'image': 'Upload a picture of the bike (JPEG, PNG).',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bike name'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'engine_cc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter engine cc'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }