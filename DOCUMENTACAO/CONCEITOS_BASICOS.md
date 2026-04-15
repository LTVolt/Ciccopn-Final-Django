# 📖 Guia: Como Funciona o Django

## 1. Estrutura do Django (Conceitos Básicos)

### A. **Settings.py** - O Coração do Projeto
Local: `config/settings.py`

Este ficheiro contém **todas as configurações** do seu projeto Django:
- Qual base de dados usar
- Que aplicações estão ativas
- Configurações de segurança
- Timezone, idioma, etc.

**Exemplo de configurações principais:**
```python
# Base de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Tipo BD
        'NAME': 'nome_da_bd',                  # Nome BD
        'USER': 'root',                        # Utilizador
        'PASSWORD': 'password',                # Senha
        'HOST': 'localhost',                   # Servidor
        'PORT': '3306',                        # Porta
    }
}

# Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',      # Painel administrativo
    'django.contrib.auth',       # Sistema de autenticação
    'imovel',                    # NOSSA APP (será adicionada)
]
```

---

### B. **Models.py** - Definir a Estrutura de Dados
Local: `imovel/models.py`

Aqui você **define como os dados estão organizados**.

**Exemplo:**
```python
from django.db import models

class Propriedade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    localizacao = models.CharField(max_length=200)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
```

**O que acontece:**
- Django cria automaticamente uma tabela no MySQL
- Cada campo (`titulo`, `descricao`, etc.) vira uma coluna
- `models.CharField` = texto curto
- `models.TextField` = texto longo
- `models.DecimalField` = números com decimais

---

### C. **Views.py** - A Lógica
Local: `imovel/views.py`

Aqui você **define o que acontece quando alguém acessa uma página**.

**Exemplo:**
```python
from django.shortcuts import render
from .models import Propriedade

def lista_propriedades(request):
    propriedades = Propriedade.objects.all()  # Busca TUDO da BD
    return render(request, 'imovel/lista.html', {
        'propriedades': propriedades
    })
```

**O que acontece:**
1. Alguém acessa a URL `/propriedades/`
2. Django executa `lista_propriedades()`
3. A função busca **todas** as propriedades da BD
4. Envia os dados para o template HTML `lista.html`

---

### D. **URLs.py** - As Rotas
Local: `config/urls.py` ou `imovel/urls.py`

Aqui você **mapeia URLs para views**.

**Exemplo:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('propriedades/', views.lista_propriedades, name='lista'),
    path('propriedades/<int:id>/', views.detalhe_propriedade, name='detalhe'),
]
```

**O que acontece:**
- `/propriedades/` → executa `lista_propriedades()`
- `/propriedades/5/` → executa `detalhe_propriedade(id=5)`

---

### E. **Templates** - O HTML
Local: `imovel/templates/imovel/`

Aqui você **cria as páginas HTML** que o utilizador vê.

**Exemplo: `lista.html`**
```html
<h1>Propriedades Disponíveis</h1>
<div>
    {% for prop in propriedades %}
        <div>
            <h2>{{ prop.titulo }}</h2>
            <p>{{ prop.descricao }}</p>
            <p>Preço: €{{ prop.preco }}</p>
        </div>
    {% endfor %}
</div>
```

**O que acontece:**
- `{{ prop.titulo }}` = mostra o título da propriedade
- `{% for %}` = ciclo através de todas as propriedades
- Django automaticamente substitui pelas dados reais

---

## 2. Fluxo Completo (do Utilizador ao Dados)

```
1. Utilizador acessa: http://localhost:8000/propriedades/
                              ↓
2. Django procura a rota em urls.py
                              ↓
3. Encontra: path('propriedades/', views.lista_propriedades)
                              ↓
4. Executa a função: lista_propriedades(request)
                              ↓
5. A função busca na BD: Propriedade.objects.all()
                              ↓
6. Django retorna dados da BD ao template: lista.html
                              ↓
7. Template substitui valores: {{ prop.titulo }}, {{ prop.preco }}
                              ↓
8. Utilizador vê a página HTML com todos os imóveis
```

---

## 3. Ciclo de Desenvolvimento

### Quando adicionar uma tabela na BD:

```
1. Criar Modelo em models.py
   ↓
2. python manage.py makemigrations
   ↓
3. python manage.py migrate
   ↓
4. Criar View em views.py
   ↓
5. Criar Template em templates/
   ↓
6. Adicionar URL em urls.py
   ↓
7. Testar no navegador
```

---

## 4. Comandos Essenciais

| Comando | O que faz |
|---------|-----------|
| `python manage.py runserver` | Inicia o servidor (http://localhost:8000) |
| `python manage.py makemigrations` | Prepara mudanças na BD |
| `python manage.py migrate` | Aplica mudanças na BD |
| `python manage.py createsuperuser` | Cria utilizador admin |
| `python manage.py shell` | Console interativa do Django |

---

## Próximo Passo

Quando tiver a informação da sua BD MySQL, vamos:
1. Configurar a conexão em `settings.py`
2. Criar modelos que refletem suas tabelas
3. Documentar cada modelo detalhadamente

**Pronto para descrever sua base de dados?**
