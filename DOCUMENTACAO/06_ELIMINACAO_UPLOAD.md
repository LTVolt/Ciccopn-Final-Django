# Passo 6: Eliminação de Anúncios e Upload de Imagens

## O que foi implementado

### 1. Upload de imagens para o modelo `Imovel`
- Adicionado o campo `imagem_principal` em `imovel/models.py`
- Foi criado um campo do tipo `ImageField` com `upload_to='imoveis/'`
- Este campo é opcional (`null=True`, `blank=True`)

### 2. Configuração de media no Django
- Em `config/settings.py` adicionámos:
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = BASE_DIR / 'media'`
- Em `config/urls.py` adicionámos a configuração para servir ficheiros de media em desenvolvimento

### 3. Formulário de anúncio atualizado
- Em `imovel/forms.py`, o `ImovelForm` agora inclui o campo `imagem_principal`
- Em `imovel/templates/imovel/form_anuncio.html`, o formulário tem agora `enctype="multipart/form-data"`
- No modo de edição, mostramos a imagem atual, se existir

### 4. Upload de ficheiros nas views
- Em `imovel/views.py`, `criar_anuncio()` e `editar_anuncio()` agora recebem `request.FILES`
- O Django guarda a imagem automaticamente quando o formulário é válido

### 5. Mostrar imagem na lista e no detalhe
- Em `imovel/templates/imovel/lista_imoveis.html`, mostramos uma miniatura da imagem quando existir
- Em `imovel/templates/imovel/detalhe_imovel.html`, mostramos a imagem principal do imóvel

### 6. Eliminação de anúncios com confirmação
- Adicionada a view `apagar_anuncio()` em `imovel/views.py`
- A rota `conta/anunciante/anuncios/<id>/apagar/` foi adicionada a `imovel/urls.py`
- Criado o template `imovel/templates/imovel/apagar_anuncio.html`
- O utilizador deve escrever a palavra `apagar` e confirmar a ação
- Há um alerta de confirmação adicional no navegador

### 7. Admin atualizado
- O `admin.py` agora permite carregar a imagem no admin
- O admin mostra uma pré-visualização da imagem no detalhe do objeto

---

## Como funciona a confirmação de eliminação

1. No painel do anunciante, clica em **Apagar** ao lado de um anúncio
2. É aberta uma página de confirmação
3. O utilizador escreve a palavra **apagar** no campo
4. Ao enviar, o Django valida o texto e elimina o anúncio

Se a palavra estiver errada, a ação não é realizada.

---

## Notas importantes

- A imagem é guardada na pasta `media/imoveis/`
- Em ambiente de produção, deve usar um servidor estático adequado para servir media
- Para já, em desenvolvimento, o Django serve `MEDIA_URL` automaticamente

---

## Ficheiros modificados

- `imovel/models.py`
- `imovel/forms.py`
- `imovel/views.py`
- `imovel/urls.py`
- `config/settings.py`
- `config/urls.py`
- `imovel/templates/imovel/form_anuncio.html`
- `imovel/templates/imovel/lista_imoveis.html`
- `imovel/templates/imovel/detalhe_imovel.html`
- `imovel/templates/imovel/apagar_anuncio.html`
- `imovel/admin.py`

---

## Testes realizados

- `python manage.py makemigrations imovel`
- `python manage.py migrate`
- `python manage.py check`

Se quiser, posso também adicionar uma segunda imagem de galeria por anúncio ou melhorar o upload com pré-visualização antes de gravar. 