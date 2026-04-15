# Passo 15: Continuar o projeto noutra máquina

## Objetivo
Garantir que o projeto Django pode ser instalado e executado noutro computador com o mínimo de problemas.

---

## 1) Pré-requisitos da nova máquina

### Obrigatórios
- Python 3.14.x (idealmente 3.14.3 para ficar igual ao ambiente atual)
- MySQL Client/Server acessível (local ou remoto)
- Git (se for clonar do repositório)

### Recomendados
- VS Code
- Extensão Python (VS Code)

---

## 2) Copiar/clonar o projeto

Se usar Git:
```bash
git clone <URL_DO_REPOSITORIO>
cd Django_IA
```

Se copiar por pasta:
- Copiar toda a pasta do projeto incluindo:
  - `manage.py`
  - pasta `config/`
  - pasta `imovel/`
  - pasta `DOCUMENTACAO/`
  - ficheiro `requirements.txt`

---

## 3) Criar ambiente virtual (fortemente recomendado)

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4) Instalar dependências

Com o ambiente virtual ativo:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Dependências principais deste projeto:
- Django 5.2.13
- mysqlclient 2.2.8
- Pillow 12.1.1

---

## 5) Configurar a ligação à base de dados

Editar `config/settings.py` e validar o bloco `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imociccopngrupo1',
        'USER': 'SEU_USER',
        'PASSWORD': 'SUA_PASSWORD',
        'HOST': 'SEU_HOST',
        'PORT': '3306',
    }
}
```

Confirmar também:
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`

---

## 6) Migrar base de dados

Se a base já existe com tabelas criadas previamente:
```bash
python manage.py migrate --fake-initial
```

Se a base for nova:
```bash
python manage.py migrate
```

---

## 7) Criar superutilizador (se necessário)

```bash
python manage.py createsuperuser
```

---

## 8) Validar e arrancar o projeto

```bash
python manage.py check
python manage.py runserver
```

Abrir no browser:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

---

## 9) Pontos críticos para evitar problemas

1. `mysqlclient` pode falhar instalação se faltarem binários/compiladores.
- Em Windows, instalar "Microsoft C++ Build Tools" se necessário.

2. Garantir que a nova máquina consegue ligar ao MySQL remoto.
- Firewall, IP permitido e credenciais corretas.

3. Confirmar que a pasta `media/` tem permissões de escrita.
- Necessário para upload de imagem principal e galeria.

4. Não usar o servidor de desenvolvimento em produção.
- `runserver` é só para desenvolvimento/testes.

---

## 10) Checklist rápido de migração

- [ ] Projeto copiado/clonado
- [ ] Ambiente virtual criado e ativo
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] `settings.py` ajustado com credenciais da BD
- [ ] Migrações executadas
- [ ] `python manage.py check` sem erros
- [ ] `python manage.py runserver` a funcionar

---

## 11) Comando único (Windows PowerShell)

Se já estiver na pasta do projeto:
```powershell
python -m venv .venv ; .\.venv\Scripts\Activate.ps1 ; pip install -U pip ; pip install -r requirements.txt ; python manage.py check ; python manage.py runserver
```

---

## 12) Próxima melhoria recomendada

Para maior segurança, mover credenciais da BD para variáveis de ambiente (em vez de deixar no `settings.py`).
