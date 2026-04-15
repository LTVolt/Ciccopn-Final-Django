# Passo 6: Filtros de pesquisa de imóveis

## Objetivo
Permitir pesquisar imóveis com filtros práticos e encadeados:

1. Localização por `Distrito` → `Concelho` → `Freguesia`.
2. Tipologia e número de WC (dropdowns de 0 a 9).
3. Preço e área com limites mínimo e máximo.

---

## O que foi implementado

### 1) Lógica de filtros no backend
Arquivo: [imovel/views.py](../imovel/views.py)

A view `lista_imoveis()` agora:
- Lê parâmetros GET (`distrito`, `concelho`, `freguesia`, `tipologia`, `numero_wc`, `preco_min`, `preco_max`, `area_min`, `area_max`).
- Valida inteiros e decimais.
- Aplica filtros no queryset de `Imovel`.
- Envia para o template listas completas de `Distrito`, `Concelho` e `Freguesia`.

Também foram adicionadas funções auxiliares:
- `_parse_int()`
- `_parse_decimal()`

Estas funções evitam erros quando o utilizador envia valores inválidos.

---

### 2) Formulário de filtros no frontend
Arquivo: [imovel/templates/imovel/lista_imoveis.html](../imovel/templates/imovel/lista_imoveis.html)

Foi criado um formulário com:
- Dropdown de Distrito.
- Dropdown de Concelho.
- Dropdown de Freguesia.
- Dropdown de Tipologia `T0..T9`.
- Dropdown de WC `0..9`.
- Inputs numéricos para preço e área min/max.

Também foi adicionado:
- Botão “Aplicar filtros”.
- Botão “Limpar filtros”.
- Contador de resultados encontrados.

---

### 3) Dropdowns dependentes (encadeamento)
No mesmo template, foi incluído JavaScript para garantir:

- Ao escolher um `Distrito`, só aparecem `Concelhos` desse distrito.
- Ao escolher um `Concelho`, só aparecem `Freguesias` desse concelho.

Isto melhora a usabilidade e evita escolhas inconsistentes.

---

## Como testar

1. Abrir [imovel/templates/imovel/lista_imoveis.html](../imovel/templates/imovel/lista_imoveis.html) via rota `/imoveis/`.
2. Testar combinações:
   - Distrito → Concelho → Freguesia.
   - Tipologia `T0..T9`.
   - Nº WC `0..9`.
   - Preço e área com intervalos.
3. Confirmar que o número de resultados muda corretamente.

---

## Resultado
A página de listagem está agora preparada para pesquisa imobiliária real, com filtros rápidos, intuitivos e consistentes com a hierarquia geográfica.
