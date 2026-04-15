# ⚠️ IMPORTANTE: Configuração de Credenciais MySQL

## O Problema

O Django tentou conectar ao MySQL mas recebeu um erro de autenticação:
```
Access denied for user 'root'@'localhost' (using password: NO)
```

**Significado:** O utilizador `root` do MySQL requer uma senha para conectar.

---

## A Solução

Você tem 2 opções:

### Opção 1: Fornecer a Senha MySQL (Recomendado) ✅
Edite o arquivo: [config/settings.py](../config/settings.py)

Procure por:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imociccopngrupo1',
        'USER': 'root',
        'PASSWORD': '',  # ← MUDE AQUI
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**Exemplo 1:** Se a senha é "minhasenhambgm"
```python
'PASSWORD': 'minhasenhambgm',
```

**Exemplo 2:** Se a senha é "123456"
```python
'PASSWORD': '123456',
```

### Opção 2: Remover a Senha do MySQL (Apenas para Desenvolvimento) ⚠️
No seu computador, abra o MySQL e remova a senha:

```sql
-- Conectar ao MySQL sem senha (pode ser preciso de admin)
mysql -u root

-- Dentro do MySQL, execute:
ALTER USER 'root'@'localhost' IDENTIFIED BY '';
FLUSH PRIVILEGES;
```

**Nota:** Esta opção é **apenas para desenvolvimento local**. Nunca faça isto num servidor de produção!

---

## 📋 Próximos Passos

1. Modifique `settings.py` com a senha correta (ou remova-a do MySQL)
2. Depois, avise-me para continuar com as migrações

---

## ⚠️ Segurança

**Importante:** Não partilhe a senha MySQL com ninguém!

Quando o projeto estiver em produção, use variáveis de ambiente:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

---

**Qual é a senha do seu MySQL?**
