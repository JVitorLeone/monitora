from django.forms import ModelForm
from django import forms
from produtos.models import Produto
    
class SortProdForm(forms.Form):
    nome = forms.CharField(label= False, required= True, widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'placeholder': 'Buscar', 'required' : True}))

class CadastroProdForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tempo_notificacao', 'preco_atual', 'url']
        widgets = {
            'url' : forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255, 'required': True, 'placeholder': "URL"}),
            'preco_atual': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255, 'required': True,}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255, 'required': True, 'placeholder': "Nome do produto"}),
            'tempo_notificacao': forms.NumberInput(attrs={'class': 'form-control', 'max': '3600', 'min': '5', 'required': False, 'null': True, 'blank': True}),
        }