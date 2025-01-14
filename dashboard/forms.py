from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','discription']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discription': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject','title','description','due','is_finished']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due': DateInput(attrs={'class': 'form-control' }),
            # 'is_finished': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class DashboradForm(forms.Form):
    text = forms.CharField(max_length = 100,label="Enter what to search")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'})
        }

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mess','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    class Meta:
        widgets = {
                'input': forms.TextInput(attrs={'class': 'form-control'}),
                'measure1': forms.Select(attrs={'class': 'form-control'}),
                'measure2': forms.Select(attrs={'class': 'form-control'}),
            }

class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    class Meta:
        widgets = {
                'input': forms.TextInput(attrs={'class': 'form-control'}),
                'measure1': forms.Select(attrs={'class': 'form-control'}),
                'measure2': forms.Select(attrs={'class': 'form-control'}),
            }

class UserRegistrationFrom(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2'] 
        