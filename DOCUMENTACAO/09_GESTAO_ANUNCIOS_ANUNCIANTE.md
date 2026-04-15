# Passo 9: Criação e edição de anúncios (apenas anunciante)

## Objetivo
Permitir que apenas contas do tipo anunciante possam criar e editar anúncios na sua área.

---

## Implementação

### 1) Formulário de anúncio
Arquivo: [imovel/forms.py](../imovel/forms.py)

Foi criado `ImovelForm` (ModelForm) para os campos:
- Morada
- Descrição
- Preço
- Tipologia (n.º quartos)
- N.º WC
- Data de construção
- Área
- Freguesia

Notas:
- `id_anunciante` não aparece no formulário (é definido automaticamente pela conta autenticada).
- Validação e widgets configurados para campos numéricos e data.

---

### 2) Views protegidas para gestão
Arquivo: [imovel/views.py](../imovel/views.py)

Foram adicionadas:
- `criar_anuncio()`
- `editar_anuncio(id_imovel)`

Regras:
- Só utilizadores com perfil `ANUNCIANTE` (ou superuser) podem criar/editar.
- Na edição, utilizador anunciante só edita anúncios associados ao seu email.
- Associação do anúncio ao anunciante é feita automaticamente por email.

---

### 3) Rotas
Arquivo: [imovel/urls.py](../imovel/urls.py)

Rotas criadas:
- `/conta/anunciante/anuncios/novo/`
- `/conta/anunciante/anuncios/<id>/editar/`

---

### 4) Painel anunciante com ações
Arquivo: [imovel/templates/imovel/painel_anunciante.html](../imovel/templates/imovel/painel_anunciante.html)

Foi adicionado:
- Botão “Criar novo anúncio”
- Botão “Editar” em cada anúncio

---

### 5) Template do formulário de anúncio
Arquivo: [imovel/templates/imovel/form_anuncio.html](../imovel/templates/imovel/form_anuncio.html)

Template único para:
- Modo criação
- Modo edição

---

## Resultado
A funcionalidade de gestão de anúncios está disponível no painel de anunciante e já respeita permissões por papel e propriedade do anúncio.
