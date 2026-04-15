from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from .models import Freguesia, Imovel, PerfilUtilizador, Anunciante, Proprietario, Consultor, Agencia


class RegistoForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Primeiro nome')
    last_name = forms.CharField(max_length=30, required=True, label='Último nome')
    telefone = forms.CharField(max_length=9, min_length=9, required=True, label='Telefone (9 dígitos)', help_text='Introduza apenas os 9 dígitos.', validators=[validators.RegexValidator(r'^\d{9}$', 'Telefone deve ter exatamente 9 dígitos.')])
    tipo_utilizador = forms.ChoiceField(
        choices=PerfilUtilizador.TIPO_CHOICES,
        initial=PerfilUtilizador.TIPO_COMUM,
        label='Tipo de conta',
    )
    tipo_anunciante = forms.ChoiceField(
        choices=Anunciante.TIPO_CHOICES,
        required=False,
        label='Tipo de anunciante',
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'tipo_utilizador', 'tipo_anunciante', 'password1', 'password2')
        labels = {
            'username': 'Nome de utilizador',
            'password1': 'Palavra-passe',
            'password2': 'Confirmar palavra-passe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make tipo_anunciante required only if tipo_utilizador is 'anunciante'
        if self.data and self.data.get('tipo_utilizador') == PerfilUtilizador.TIPO_ANUNCIANTE:
            self.fields['tipo_anunciante'].required = True
        elif self.initial and self.initial.get('tipo_utilizador') == PerfilUtilizador.TIPO_ANUNCIANTE:
            self.fields['tipo_anunciante'].required = True

    def clean(self):
        cleaned_data = super().clean()
        tipo_utilizador = cleaned_data.get('tipo_utilizador')
        tipo_anunciante = cleaned_data.get('tipo_anunciante')
        if tipo_utilizador == PerfilUtilizador.TIPO_ANUNCIANTE and not tipo_anunciante:
            raise forms.ValidationError("Tipo de anunciante é obrigatório para contas de anunciante.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create PerfilUtilizador
            from .views import _get_or_create_perfil  # Import here to avoid circular import
            perfil = _get_or_create_perfil(user)
            perfil.tipo_utilizador = self.cleaned_data['tipo_utilizador']
            perfil.save()
            # If advertiser, create Anunciante
            if perfil.is_anunciante:
                nome_completo = f"{user.first_name} {user.last_name}"
                telefone_com_prefixo = f"+351{self.cleaned_data['telefone']}"
                tipo_anunciante = int(self.cleaned_data['tipo_anunciante'])
                # Create the related entity based on tipo_anunciante
                if tipo_anunciante == 1:  # Proprietário
                    proprietario = Proprietario.objects.create(nome=nome_completo)
                    Anunciante.objects.create(
                        email=user.email,
                        telefone=telefone_com_prefixo,
                        tipo=tipo_anunciante,
                        id_proprietario=proprietario
                    )
                elif tipo_anunciante == 2:  # Consultor
                    consultor = Consultor.objects.create(nome=nome_completo)
                    Anunciante.objects.create(
                        email=user.email,
                        telefone=telefone_com_prefixo,
                        tipo=tipo_anunciante,
                        id_consultor=consultor
                    )
                elif tipo_anunciante == 3:  # Agência
                    agencia = Agencia.objects.create(nome=nome_completo)
                    Anunciante.objects.create(
                        email=user.email,
                        telefone=telefone_com_prefixo,
                        tipo=tipo_anunciante,
                        id_agencia=agencia
                    )
        return user


class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = (
            'morada',
            'descricao',
            'preco',
            'numero_quartos',
            'numero_wc',
            'imagem_principal',
            'data_construcao',
            'area',
            'id_freguesia',
        )
        labels = {
            'morada': 'Morada',
            'descricao': 'Descrição',
            'preco': 'Preço (€)',
            'numero_quartos': 'Tipologia (n.º quartos)',
            'numero_wc': 'Número de WC',
            'imagem_principal': 'Imagem principal',
            'data_construcao': 'Data de construção',
            'area': 'Área (m²)',
            'id_freguesia': 'Freguesia',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'data_construcao': forms.DateInput(attrs={'type': 'date'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'area': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'numero_quartos': forms.NumberInput(attrs={'min': '0', 'max': '9'}),
            'numero_wc': forms.NumberInput(attrs={'min': '0', 'max': '9'}),
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'data_construcao': forms.DateInput(attrs={'type': 'date'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'area': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'numero_quartos': forms.NumberInput(attrs={'min': '0', 'max': '9'}),
            'numero_wc': forms.NumberInput(attrs={'min': '0', 'max': '9'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_freguesia'].queryset = Freguesia.objects.select_related('id_concelho').order_by('nome')
