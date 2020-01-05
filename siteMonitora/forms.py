from users.models import Usuario
from bootstrap_modal_forms.forms import BSModalForm

class LoginForm(BSModalForm):
    class Meta:
        model = Usuario
        fields = ['login', 'senha']