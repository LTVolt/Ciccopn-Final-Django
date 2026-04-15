# 📖 Passo 2: Configuração do MySQL e Django

## Objetivo
Conectar o Django à sua base de dados MySQL existente.

---

## O que foi Configurado

### 1. **mysqlclient** instalado
- Driver que permite Python/Django comunicar com MySQL
- Equivalente ao `mysql-connector-python` mas mais rápido

### 2. **settings.py** atualizado
Arquivo: [config/settings.py](config/settings.py)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imociccopngrupo1',      # Base de dados
        'USER': 'root',                  # Utilizador MySQL
        'PASSWORD': '',                  # Senha (modificar se tiver)
        'HOST': 'localhost',             # Servidor
        'PORT': '3306',                  # Porta padrão
    }
}
```

### 3. **Configurações de Localização**
```python
LANGUAGE_CODE = 'pt-pt'              # Português de Portugal
TIME_ZONE = 'Europe/Lisbon'          # Timezone Lisboa
```

---

## ⚙️ Se a Sua Configuração for Diferente

### Cenário: MySQL num servidor remoto
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imociccopngrupo1',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': '192.168.1.100',  # IP do servidor
        'PORT': '3306',
    }
}
```

### Cenário: MySQL com porta diferente
```python
'PORT': '3307',  # Se MySQL está em porta diferente
```

### Cenário: Sem senha no MySQL (como está agora)
```python
'PASSWORD': '',  # Deixar vazio
```

---

## 🔍 Como Testar a Conexão

Abra o terminal PowerShell e execute:

```powershell
cd "C:\Users\Public\Documents\C Coding\Misc\Coding\Python\Final\Django_IA"
python manage.py shell
```

Depois, no console Python do Django:

```python
# Importar a configuração da BD
from django.conf import settings
print(settings.DATABASES)

# Tentar conectar (verá erro se não conectar)
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())

# Sair
exit()
```

Se aparecer a versão do MySQL, a conexão está **OK** ✅

---

## 📋 Checklist de Configuração

- [x] `mysqlclient` instalado
- [x] `settings.py` configurado com dados MySQL
- [x] `LANGUAGE_CODE` = pt-pt (português)
- [x] `TIME_ZONE` = Europe/Lisbon (Lisboa)
- [ ] **Próximo**: Executar migrações

---

## 🎯 Próximas Etapas

1. Testar a conexão (opcional, mas recomendado)
2. Executar `python manage.py migrate` (próximo passo)

**Tudo pronto? Vamos sincronizar os modelos com a BD!**
