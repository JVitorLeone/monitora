from django.forms import ModelForm
from django import forms
from .models import Usuario
from django.contrib.auth.models import User

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 64}),
        }

    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'telefone',
                  'data_nascimento']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True}),
            'telefone': forms.TextInput(attrs={'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control loginInput cadastroInput', 'maxlength': 255, 'required': True},format="%d/%m/%Y"),
    
        }


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control loginInput col-10', 'maxlength': 64, 'required': True, 'autofocus': True, 'placeholder': "Usuário"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control loginInput col-10', 'maxlength': 255, 'required': True, 'placeholder': "Senha"}),
        }

        error_messages = {
            'password': {
                'required': 'Este campo é obrigatório',
            },
        }
