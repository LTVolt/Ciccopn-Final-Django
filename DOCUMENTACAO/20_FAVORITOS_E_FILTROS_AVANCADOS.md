# Passo 20: Favoritos por utilizador e filtros avançados

## Objetivo
Adicionar uma funcionalidade de favoritos por utilizador (com estrela nos cartões de imóveis) e evoluir a pesquisa com novos filtros e ordenação.

---

## O que foi implementado

1. Favoritos por utilizador autenticado
- Cada cartão de imóvel passou a incluir uma estrela no canto superior direito.
- Clique na estrela alterna entre:
  - estrela vazia (não favoritado);
  - estrela preenchida (favoritado).
- O estado fica persistido por utilizador na base de dados.

2. Novo modelo de favoritos
- Foi criado o modelo `Favorito` para relacionar `User` e `Imovel`.
- Foi aplicada restrição de unicidade por par (`user`, `id_imovel`) para evitar duplicados.

3. Endpoint de toggle de favorito
- Foi criada rota dedicada para adicionar/remover favorito.
- O comportamento suporta resposta assíncrona (AJAX) para atualizar o estado da estrela sem recarregar página.

4. Favoritos nas dashboards
- A dashboard de conta comum passou a mostrar:
  - total de favoritos;
  - lista dos imóveis favoritos.
- O painel de anunciante passou a mostrar:
  - total de favoritos;
  - lista dos imóveis favoritos.

5. Filtro apenas favoritos na pesquisa
- Foi adicionada checkbox "Mostrar apenas favoritos" na listagem.
- Quando ativa (e com sessão iniciada), a pesquisa devolve apenas os imóveis favoritados pelo utilizador atual.

6. Ordenação avançada na pesquisa
- Dropdown "Ordenar por" com as opções:
  - Mais recentes (padrão)
  - Preço: ascendente
  - Preço: descendente
  - Área: ascendente
  - Área: descendente
  - Data de construção: mais antigo
  - Data de construção: mais recente

---

## Ficheiros alterados

- `imovel/models.py`
- `imovel/admin.py`
- `imovel/views.py`
- `imovel/urls.py`
- `imovel/templates/imovel/lista_imoveis.html`
- `imovel/templates/imovel/perfil.html`
- `imovel/templates/imovel/painel_anunciante.html`
- `imovel/migrations/0005_favorito.py`

---

## Resultado

A plataforma passou a permitir personalização da navegação por utilizador através de favoritos persistentes e tornou a pesquisa mais útil com filtro de favoritos e ordenação flexível.
