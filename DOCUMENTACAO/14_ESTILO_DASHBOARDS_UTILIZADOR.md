# Passo 14: Modernização visual das dashboards (utilizador e anunciante)

## Objetivo
Atualizar o estilo da área pessoal (conta normal) e do painel de anunciante para uma linguagem visual mais moderna e consistente com os passos anteriores.

---

## O que foi alterado

1. Dashboard de utilizador normal (`perfil.html`)
- Hero com gradiente e contexto da área pessoal.
- Cartões de métricas (utilizador, email, tipo de conta).
- Ações rápidas com botões mais claros.
- Secção de últimos imóveis com cartões leves.

2. Dashboard de anunciante (`painel_anunciante.html`)
- Hero visual semelhante para consistência de interface.
- KPIs principais em cartões (conta, tipo, total de imóveis).
- Bloco de ações rápidas (criar anúncio / ver pesquisa pública).
- Lista de imóveis em formato de cartões individuais com ações diretas:
  - editar
  - apagar

3. Responsividade
- Layout adaptado para ecrãs pequenos, mantendo legibilidade e usabilidade.

---

## Ficheiros alterados

- `imovel/templates/imovel/perfil.html`
- `imovel/templates/imovel/painel_anunciante.html`

---

## Resultado

As duas dashboards passam a ter:
- hierarquia visual mais forte,
- melhor leitura de informação,
- consistência estética com o restante projeto,
- ações mais fáceis de encontrar.

---

## Validação

Comando executado:
- `python manage.py check`

Resultado:
- Sem erros.
