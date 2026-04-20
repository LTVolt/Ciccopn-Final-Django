# Passo 23: Pesquisa por distrito através de mapa interativo

## Objetivo
Criar uma entrada visual para a pesquisa de imóveis, sem alterar o fluxo atual da listagem, permitindo ao utilizador escolher o distrito clicando num mapa de Portugal Continental.

---

## Estratégia adotada

Foi criada uma página nova e isolada em vez de substituir os filtros existentes na listagem.

Isto reduz risco porque:

- a view principal de pesquisa mantém o mesmo comportamento;
- o filtro final continua a ser o mesmo parâmetro `distrito` na URL;
- o mapa apenas constrói um link de retorno para `imovel:lista_imoveis`.

---

## O que foi implementado

1. Nova rota para pesquisa por mapa
- URL: `imoveis/mapa/`
- View dedicada: `mapa_distritos`

2. Botão na página de pesquisa atual
- Foi adicionado um botão na listagem para abrir o mapa.
- Os filtros já selecionados são preservados na query string.

3. Mapa interativo de Portugal Continental
- Foi adicionado um SVG local com os 18 distritos do continente.
- Cada distrito fica clicável e encaminha o utilizador de volta para a listagem com o filtro `distrito` aplicado.

4. Lista lateral de fallback
- A página do mapa inclui também uma lista de distritos clicável.
- Serve como alternativa caso o SVG não carregue corretamente num determinado dispositivo.

---

## Referências consultadas

1. Leaflet choropleth tutorial
- https://leafletjs.com/examples/choropleth/
- Usado como referência de interação por regiões: hover, destaque e clique.

2. geoBoundaries Portugal ADM1
- https://www.geoboundaries.org/api/current/gbOpen/PRT/ADM1/
- Confirmou a disponibilidade de fronteiras administrativas abertas para Portugal como alternativa baseada em GeoJSON.

3. SimpleMaps Portugal SVG admin1
- https://simplemaps.com/resources/svg-pt
- Fonte do SVG base adaptado para a versão local do mapa.

---

## Decisão técnica

Apesar de ser possível usar Leaflet com GeoJSON, nesta fase foi preferida a solução em SVG local porque:

- introduz menos dependências externas;
- é mais simples de manter;
- é mais segura para um projeto que já está numa fase avançada;
- resolve o requisito de clique por distrito com menor risco de regressão.