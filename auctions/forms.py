from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import AuctionListing, User, AbstractUser


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'category', 'image', 'price', 'active', 'owner']
        title = {'title': 'title', 
                 'description': 'description', 
                 'category':'category',
                 'image': 'image',
                 'price':'price',
                 'active': 'active',
                }
        widgets ={'description': forms.Textarea(attrs={'class':'form-control'}),
                  'title': forms.TextInput(attrs={'class':'form-control'}),
                  #we used hidden input to make the owner field immutable.
                  'owner': forms.HiddenInput(),
                }
    #to autofill the owner field with the current_user we used the contsructor method            
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        if current_user:
            #here we are setting the initial value of the owner field to the current user.
            self.fields['owner'].initial = current_user
            