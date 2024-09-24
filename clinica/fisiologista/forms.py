from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import User
from .models import Appointment


TIME_CHOICES = [
    ("09:00", "09:00"),
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("12:00", "12:00"),
    ("13:00", "13:00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
    ("16:00", "16:00"),
    ("17:00", "17:00"),
]

class UserRegistrationForm(UserCreationForm):

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'gender-option'}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'cpf', 'email', 'password1', 'password2', 'phone', 'birth', 'gender', 'adress', 'cep']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-box'}),
            'last_name': forms.TextInput(attrs={'class': 'input-box'}),
            'username': forms.TextInput(attrs={'class': 'input-box'}),
            'cpf': forms.TextInput(attrs={'class': 'input-box', 'id': 'CPF'}),
            'email': forms.EmailInput(attrs={'class': 'input-box'}),
            'password1': forms.PasswordInput(attrs={'class': 'input-box'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-box'}),
            'phone': forms.TextInput(attrs={'class': 'input-box', 'id':'telefone'}),
            'birth': forms.DateInput(attrs={'class': 'input-box', 'type': 'date'}),
            'adress': forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Endereço'}),
            'cep': forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'CEP', 'id': 'CEP', 'maxlength': '9'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-box'}),
            'password': forms.PasswordInput(attrs={'class': 'input-box'}),
        }


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['data', 'time', 'tipo_tratamento', 'professional', 'resumo_problemas']
        widgets = {
            'data': forms.DateInput(attrs={'type':'date', 'id': 'date'}),
            'time': forms.Select(choices=TIME_CHOICES, attrs={'id': 'time'}),
            'tipo_tratamento': forms.Select(attrs={'id': 'specialty'}),
            'resumo_problemas': forms.Textarea(attrs={'id': 'reason', 'rows': 4}),
        }