from django import forms
from .models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MyRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

class StockForm(forms.ModelForm):
    def save(self,user=None, force_insert=False, force_update=False, commit=True):
        q = super(StockForm, self).save(commit=False)
        q.user = user
        if commit:
            q.save()
        return q
    class Meta:
        model = Stock
        exclude = ('user',)
