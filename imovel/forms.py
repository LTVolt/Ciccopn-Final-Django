from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.db import transaction
from django.db.models import Max

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
            with transaction.atomic():
                user.save()
                # Create PerfilUtilizador
                from .views import _get_or_create_perfil  # Import here to avoid circular import
                perfil = _get_or_create_perfil(user)
                perfil.tipo_utilizador = self.cleaned_data['tipo_utilizador']
                perfil.telefone = self.cleaned_data['telefone']
                perfil.save()
                # If advertiser, create Anunciante
                if perfil.is_anunciante:
                    nome_completo = f"{user.first_name} {user.last_name}"
                    telefone_com_prefixo = f"+351{self.cleaned_data['telefone']}"
                    tipo_anunciante = int(self.cleaned_data['tipo_anunciante'])
                    # Create the related entity based on tipo_anunciante
                    if tipo_anunciante == 1:  # Proprietário
                        max_id = Proprietario.objects.aggregate(max_id=Max('id_proprietario')).get('max_id') or 0
                        proprietario = Proprietario.objects.create(
                            id_proprietario=max_id + 1,
                            nome=nome_completo,
                        )
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_freguesia'].queryset = Freguesia.objects.select_related('id_concelho').order_by('nome')


class ContaPerfilForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Nome de utilizador')
    first_name = forms.CharField(max_length=30, required=True, label='Primeiro nome')
    last_name = forms.CharField(max_length=30, required=True, label='Último nome')
    email = forms.EmailField(required=True, label='Email')
    telefone = forms.CharField(
        max_length=9,
        min_length=9,
        required=False,
        label='Telefone (9 dígitos)',
        help_text='Introduza apenas os 9 dígitos (sem +351).',
        validators=[validators.RegexValidator(r'^\d{9}$', 'Telefone deve ter exatamente 9 dígitos.')],
    )
    receber_notificacoes_email = forms.BooleanField(
        required=False,
        label='Receber notificações por email',
    )

    def __init__(self, user, perfil, *args, **kwargs):
        self.user = user
        self.perfil = perfil
        super().__init__(*args, **kwargs)

        telefone_inicial = (perfil.telefone or '').strip()
        if not telefone_inicial:
            anunciante = Anunciante.objects.filter(email__iexact=user.email).first()
            if anunciante and anunciante.telefone:
                telefone_inicial = anunciante.telefone.strip()
                if telefone_inicial.startswith('+351'):
                    telefone_inicial = telefone_inicial[4:]

        self.fields['username'].initial = user.username
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['telefone'].initial = telefone_inicial
        self.fields['receber_notificacoes_email'].initial = perfil.receber_notificacoes_email

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if not username:
            raise forms.ValidationError('Nome de utilizador é obrigatório.')
        existe = User.objects.filter(username__iexact=username).exclude(pk=self.user.pk).exists()
        if existe:
            raise forms.ValidationError('Já existe um utilizador com esse nome.')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise forms.ValidationError('Email é obrigatório.')
        existe = User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists()
        if existe:
            raise forms.ValidationError('Já existe uma conta com esse email.')
        return email

    def save(self):
        old_email = self.user.email
        telefone = (self.cleaned_data.get('telefone') or '').strip()

        self.user.username = self.cleaned_data['username']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        self.perfil.telefone = telefone
        self.perfil.receber_notificacoes_email = self.cleaned_data.get('receber_notificacoes_email', False)
        self.perfil.save()

        anunciante_qs = Anunciante.objects.filter(email__iexact=old_email)
        if not anunciante_qs.exists():
            anunciante_qs = Anunciante.objects.filter(email__iexact=self.user.email)

        if anunciante_qs.exists():
            updates = {'email': self.user.email}
            if telefone:
                updates['telefone'] = f'+351{telefone}'
            anunciante_qs.update(**updates)

        return self.user
