from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from time import sleep
from django.contrib.gis import forms as gis_forms
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

COLOR_CHOICES=(
    ('Black and White','Black and White'),
    ('Colored','Colored')

    )
class PlaceOrderForm(ModelForm):
    #Color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Order
        labels = {"docfile":"Document","type":"Color Option"}
        fields = ['docfile','shop', 'quantity' ,'type','size','notes','buyer']
        widgets = {'shop': forms.HiddenInput(),
        'buyer': forms.HiddenInput(),
        'type' : forms.RadioSelect()
        }
#widget=models.OSMWidget(attrs={'map_width': 800, 'map_height': 500})
class CreateShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['name','location', 'city' ,'address','owner']
        labels = {"name":"Shop name","location":"Shop location"}
        widgets = {'owner': forms.HiddenInput(),'location':gis_forms.OSMWidget(attrs={ 'map_height': 500,'default_lat':29.3353,'default_lon':48.0716})}

class OwnerCreateForm(UserCreationForm):
    isOwner = forms.BooleanField(widget=forms.HiddenInput())
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",'isOwner')
        #widgets = {'isOwner': forms.HiddenInput()}
    def save(self, commit=True):
        user = super(OwnerCreateForm, self).save(commit=False)
        print(self.cleaned_data["isOwner"])
        if commit:
            user.save()
        user.profile.isOwner = self.cleaned_data["isOwner"]
        user.save()
        return user