# 📚 Passo 1: Setup Inicial do Django

## Objetivo
Configurar o projeto Django básico para um site imobiliário.

---

## O que foi criado?

### 1. **Estrutura do Projeto**
```
Django_IA/
├── manage.py              # Arquivo para executar comandos Django
├── config/                # Pasta de configuração principal
│   ├── __init__.py
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py            # Rotas do projeto
│   ├── asgi.py            # Configuração para deploy
│   └── wsgi.py            # Configuração para deploy
├── imovel/                # Aplicação de imóveis
│   ├── migrations/        # Controle de versão da BD
│   ├── admin.py           # Configuração do painel admin
│   ├── apps.py            # Configuração da app
│   ├── models.py          # Modelos de dados (IMPORTANTE!)
│   ├── tests.py           # Testes
│   ├── views.py           # Lógica de visualização
│   └── __init__.py
└── DOCUMENTACAO/          # Esta pasta com guias
```

---

## Próximos Passos

1. ✅ Setup inicial criado
2. ⏳ **PASSO 2**: Configurar a conexão ao MySQL
3. ⏳ PASSO 3: Criar modelos baseados na sua BD
4. ⏳ PASSO 4: Criar views para mostrar dados
5. ⏳ PASSO 5: Criar templates HTML

---

## Arquivos Importantes Neste Momento

### `manage.py`
- **O quê**: Script principal do Django
- **Como usar**: 
  ```bash
  python manage.py runserver        # Iniciar o servidor
  python manage.py makemigrations   # Preparar mudanças na BD
  python manage.py migrate          # Aplicar mudanças na BD
  ```

### `config/settings.py`
- **O quê**: Configurações gerais do projeto
- **O que contém**: 
  - Apps instaladas
  - Configuração da BD
  - Secret key
  - Timezone
  - Etc.

---

## Próxima Ação

Quando reunir a informação da sua base de dados MySQL, vou:
1. Configurar a conexão ao MySQL
2. Criar os modelos baseados nas suas tabelas
3. Documentar cada modelo

**Informação necessária:**
- Nome da BD MySQL
- Nomes das tabelas
- Estrutura das tabelas (colunas, tipos de dados)
