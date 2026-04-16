# Passo 21: Popularidade por imóvel (contador de cliques)

## Objetivo
Medir a popularidade de cada imóvel através do número de acessos ao detalhe e disponibilizar ordenação por popularidade na pesquisa.

---

## O que foi implementado

1. Contador de cliques no modelo de imóvel
- Foi adicionado o campo `contador_cliques` no modelo `Imovel`.
- Valor inicial definido como `0`.

2. Incremento automático no detalhe
- Sempre que a página de detalhe de um imóvel é aberta, o contador incrementa em +1.
- O incremento é feito no backend para contar visitas de:
  - utilizadores autenticados;
  - visitantes não autenticados.

3. Incremento seguro para acessos concorrentes
- A atualização do contador utiliza expressão atómica no lado da base de dados para evitar perdas em acessos simultâneos.

4. Ordenação por popularidade
- A pesquisa de imóveis recebeu nova opção no dropdown de ordenação:
  - Popularidade: mais vistos
- Esta ordenação utiliza o `contador_cliques` de forma decrescente.

5. Visualização da popularidade no UI
- A lista de imóveis mostra o número de visualizações por imóvel.
- A página de detalhe também exibe o valor atual de popularidade.

---

## Ficheiros alterados

- `imovel/models.py`
- `imovel/views.py`
- `imovel/templates/imovel/lista_imoveis.html`
- `imovel/templates/imovel/detalhe_imovel.html`
- `imovel/migrations/0006_imovel_contador_cliques.py`

---

## Resultado

Agora é possível acompanhar popularidade de cada imóvel com dados reais de navegação e ordenar a pesquisa para destacar os imóveis mais vistos.
