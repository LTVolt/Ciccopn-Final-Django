# Passo 12: Galeria Multi-fotos por Anuncio

## Objetivo
Permitir varias fotos por anuncio (limite de 40) e navegação por setas diretamente na listagem de imoveis.

---

## O que foi implementado

1. Novo modelo `ImovelImagem` para galeria.
2. Upload multiplo no formulario de criar/editar anuncio.
3. Limite maximo de 40 imagens por anuncio (validado no backend).
4. Galeria com setas na pagina de pesquisa/listagem.
5. Exibicao da galeria no detalhe do anuncio.
6. Suporte no admin para gerir imagens da galeria.

---

## Modelo criado

Ficheiro: `imovel/models.py`

Modelo novo:
- `ImovelImagem`
  - `id_imagem` (PK)
  - `id_imovel` (FK para `Imovel`)
  - `imagem` (`ImageField`)
  - `ordem` (para controlar sequencia)
  - `criada_em`

Tabela criada via migração:
- `imovel_imagem`

---

## Upload multiplo no formulario

Ficheiro: `imovel/forms.py`

- Criado widget `MultiFileInput` com `allow_multiple_selected = True`.
- Campo novo no `ImovelForm`:
  - `galeria_imagens` (aceita multiplos ficheiros de imagem).

---

## Regras de negocio

Ficheiro: `imovel/views.py`

- Constante: `MAX_IMAGENS_POR_ANUNCIO = 40`
- Funcao auxiliar `_guardar_imagens_galeria(...)` para gravar uploads.
- Em `criar_anuncio`:
  - bloqueia upload acima de 40.
- Em `editar_anuncio`:
  - permite adicionar fotos mantendo limite total de 40.

---

## Galeria na pesquisa (lista de imoveis)

Ficheiro: `imovel/templates/imovel/lista_imoveis.html`

- Cada card de imovel mostra 1 imagem de cada vez.
- Setas esquerda/direita alteram foto localmente no card.
- Contador visual `foto_atual/total` por anuncio.
- Se nao houver galeria, usa `imagem_principal` como fallback.

---

## Admin

Ficheiro: `imovel/admin.py`

- Inline `ImovelImagemInline` adicionado ao admin de `Imovel`.
- Pre-visualizacao de cada imagem no admin.

---

## Migrações e validacao

Comandos executados:
- `python manage.py makemigrations imovel`
- `python manage.py migrate`
- `python manage.py check`

Resultado:
- Tudo aplicado com sucesso, sem erros.
