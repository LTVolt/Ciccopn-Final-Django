# 📝 Fase 12: Registo Aprimorado para Anunciantes

## 🎯 Objetivo
Melhorar o processo de registo para garantir que anunciantes sejam automaticamente adicionados à base de dados como anunciantes válidos, permitindo-lhes criar anúncios imediatamente após o registo.

## 🔧 Implementação

### Problema Identificado
- Anunciantes registados não conseguiam criar anúncios porque o seu email não existia na tabela `anunciante`
- Era necessário adicionar manualmente os anunciantes na BD para que funcionasse

### Solução Implementada

#### 1. Atualização do Formulário de Registo (`imovel/forms.py`)
```python
class RegistoForm(UserCreationForm):
    # Campos adicionais
    first_name = forms.CharField(max_length=30, required=True, label='Primeiro nome')
    last_name = forms.CharField(max_length=30, required=True, label='Último nome')
    telefone = forms.CharField(
        max_length=9, min_length=9, required=True,
        label='Telefone (9 dígitos)',
        help_text='Introduza apenas os 9 dígitos.',
        validators=[validators.RegexValidator(r'^\d{9}$', 'Telefone deve ter exatamente 9 dígitos.')]
    )
    tipo_anunciante = forms.ChoiceField(
        choices=Anunciante.TIPO_CHOICES,
        required=False,
        label='Tipo de anunciante',
    )
```

#### 2. Lógica Condicional
- Campo `tipo_anunciante` só é obrigatório quando `tipo_utilizador` = 'ANUNCIANTE'
- Validação personalizada no método `clean()`
- JavaScript no template para mostrar/esconder o campo dinamicamente

#### 3. Criação Automática de Anunciante
No método `save()` do formulário:
```python
if perfil.is_anunciante:
    nome_completo = f"{user.first_name} {user.last_name}"
    telefone_com_prefixo = f"+351{self.cleaned_data['telefone']}"
    tipo_anunciante = int(self.cleaned_data['tipo_anunciante'])
    
    # Cria entidade relacionada (Proprietario/Consultor/Agencia)
    if tipo_anunciante == 1:  # Proprietário
        proprietario = Proprietario.objects.create(nome=nome_completo)
        Anunciante.objects.create(
            email=user.email,
            telefone=telefone_com_prefixo,
            tipo=tipo_anunciante,
            id_proprietario=proprietario
        )
    # ... similar para Consultor e Agencia
```

#### 4. Template Atualizado (`imovel/templates/imovel/registo.html`)
- Campos renderizados individualmente (não mais `form.as_p`)
- JavaScript para mostrar campo `tipo_anunciante` apenas quando necessário
- Validação visual e feedback de erros

## 📊 Resultado
- ✅ Anunciantes podem agora registar-se e criar anúncios imediatamente
- ✅ Dados pessoais (nome, telefone) são recolhidos no registo
- ✅ Prefixo +351 é adicionado automaticamente ao telefone
- ✅ Tipo de anunciante é escolhido de dropdown baseado na BD
- ✅ Validação rigorosa dos campos
- ✅ Interface responsiva com JavaScript

## 🧪 Testes Realizados
- Registo de conta comum: funciona normalmente
- Registo de anunciante: campos adicionais aparecem, validação funciona
- Criação de anúncio após registo: agora funciona sem problemas
- Validação de telefone: rejeita números inválidos
- Verificação na BD: anunciante criado corretamente com entidades relacionadas

## 📁 Ficheiros Modificados
- `imovel/forms.py` - Formulário de registo aprimorado
- `imovel/views.py` - Lógica de registo simplificada
- `imovel/templates/imovel/registo.html` - Template atualizado
- `DOCUMENTACAO/00_CHECKLIST.md` - Nova fase adicionada

---
*Próxima fase: Eliminação de anúncios com confirmação e upload de imagens*