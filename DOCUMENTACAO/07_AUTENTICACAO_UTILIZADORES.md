# Passo 7: Sistema de utilizadores (registo + login)

## Objetivo
Adicionar autenticação para que cada utilizador tenha a sua área pessoal.

---

## O que foi implementado

### 1) Formulário de registo
Arquivo: [imovel/forms.py](../imovel/forms.py)

- Foi criado o `RegistoForm`, baseado em `UserCreationForm` do Django.
- Campos usados:
  - `username`
  - `email`
  - `password1`
  - `password2`
- Ao guardar, o email é persistido no utilizador.

---

### 2) Novas views de autenticação
Arquivo: [imovel/views.py](../imovel/views.py)

Foram adicionadas as views:
- `registo()`
  - Cria conta e faz login automático após sucesso.
- `login_utilizador()`
  - Faz autenticação com `AuthenticationForm`.
  - Suporta redirecionamento por `next`.
- `logout_utilizador()`
  - Termina sessão (POST) e redireciona para início.
- `perfil()`
  - Página protegida com `@login_required`.

Também foram adicionadas mensagens com `django.contrib.messages`.

---

### 3) Novas rotas
Arquivo: [imovel/urls.py](../imovel/urls.py)

Rotas criadas:
- `/conta/registo/`
- `/conta/login/`
- `/conta/perfil/`
- `/conta/logout/`

---

### 4) Configuração global de autenticação
Arquivo: [config/settings.py](../config/settings.py)

Definições adicionadas:
- `LOGIN_URL = 'imovel:login'`
- `LOGIN_REDIRECT_URL = 'imovel:perfil'`
- `LOGOUT_REDIRECT_URL = 'imovel:home'`

---

### 5) Templates de autenticação
Arquivos:
- [imovel/templates/imovel/login.html](../imovel/templates/imovel/login.html)
- [imovel/templates/imovel/registo.html](../imovel/templates/imovel/registo.html)
- [imovel/templates/imovel/perfil.html](../imovel/templates/imovel/perfil.html)

E atualização de navegação em:
- [imovel/templates/imovel/base.html](../imovel/templates/imovel/base.html)

No menu:
- Se autenticado: link para área pessoal + botão terminar sessão.
- Se não autenticado: links para entrar e criar conta.

---

## Como testar

1. Abrir `/conta/registo/` e criar nova conta.
2. Confirmar redirecionamento para `/conta/perfil/`.
3. Terminar sessão no menu.
4. Entrar novamente em `/conta/login/`.
5. Tentar abrir `/conta/perfil/` sem login para validar proteção.

---

## Resultado
O projeto já tem um fluxo completo de autenticação e uma área pessoal inicial, totalmente integrada com a base de dados MySQL através das tabelas de autenticação do Django.
