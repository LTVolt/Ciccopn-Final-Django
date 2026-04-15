# Passo 11: Eliminação de Anúncios e Upload de Imagens

## Objetivo
Adicionar segurança na eliminação de anúncios e permitir upload de imagem principal na criação/edição de imóveis.

---

## Resumo funcional

1. O anunciante consegue eliminar um anúncio apenas após confirmação explícita.
2. A confirmação exige escrever a palavra `apagar`.
3. O formulário de anúncio passou a aceitar ficheiros de imagem.
4. A imagem enviada fica guardada em `media/imoveis/`.
5. A imagem aparece na lista, no detalhe e no admin.

---

## Implementação por ficheiro

### 1) Modelo
Ficheiro: `imovel/models.py`

No modelo `Imovel` foi adicionado:

```python
imagem_principal = models.ImageField(upload_to='imoveis/', null=True, blank=True)
```

Impacto:
- Campo opcional.
- Django gere automaticamente caminho e nome do ficheiro.

### 2) Formulário de anúncio
Ficheiro: `imovel/forms.py`

No `ImovelForm`:
- Campo `imagem_principal` incluído em `fields`.
- Label adicionada para melhor UX.

### 3) Views
Ficheiro: `imovel/views.py`

Mudanças:
- `criar_anuncio()` recebe `request.FILES`.
- `editar_anuncio()` recebe `request.FILES`.
- Nova view `apagar_anuncio()`:
  - valida permissões do utilizador;
  - valida propriedade do anúncio (ou superuser);
  - exige `confirmacao == 'apagar'`;
  - elimina registo e mostra mensagem.

### 4) Rotas
Ficheiro: `imovel/urls.py`

Nova rota:

```python
path('conta/anunciante/anuncios/<int:id_imovel>/apagar/', views.apagar_anuncio, name='apagar_anuncio')
```

### 5) Templates
Ficheiros:
- `imovel/templates/imovel/form_anuncio.html`
- `imovel/templates/imovel/painel_anunciante.html`
- `imovel/templates/imovel/lista_imoveis.html`
- `imovel/templates/imovel/detalhe_imovel.html`
- `imovel/templates/imovel/apagar_anuncio.html`

Alterações-chave:
- Formulário com `enctype="multipart/form-data"`.
- Botão `Apagar` no painel do anunciante.
- Página de confirmação com input obrigatório `apagar`.
- Exibição da imagem em lista e detalhe.

### 6) Configuração de media
Ficheiros:
- `config/settings.py`
- `config/urls.py`

Adicionado:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

E, em desenvolvimento (`DEBUG=True`), servir media via `static()`.

### 7) Admin
Ficheiro: `imovel/admin.py`

- Campo de imagem incluído no form do admin.
- Pré-visualização da imagem adicionada em readonly field.

---

## Migração aplicada

Comandos executados:
- `python manage.py makemigrations imovel`
- `python manage.py migrate`

Migração gerada:
- `imovel/migrations/0003_imovel_imagem_principal.py`

---

## Validação

Comando executado:
- `python manage.py check`

Resultado:
- Sem erros.

---

## Teste manual recomendado

1. Entrar como anunciante.
2. Criar anúncio com imagem.
3. Editar anúncio e trocar imagem.
4. Confirmar imagem em:
   - lista de imóveis;
   - detalhe de imóvel;
   - admin.
5. Clicar em apagar e testar:
   - texto errado (não deve apagar);
   - texto `apagar` (deve apagar).

---

## Observações de segurança

- A confirmação por palavra reduz eliminações acidentais.
- Em produção, ficheiros media devem ser servidos por servidor dedicado (Nginx/Apache/CDN), não por `static()` do Django.
