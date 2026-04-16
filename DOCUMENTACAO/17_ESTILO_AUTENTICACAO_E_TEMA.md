# Passo 17: Estilo de autenticação + tema claro/escuro com persistência

## Objetivo
Modernizar as páginas de autenticação (login e registo) para manter consistência visual com o restante produto e implementar alternância de tema (claro/escuro) com persistência em LocalStorage.

---

## O que foi implementado

1. Modernização de login e registo
- Layout mais moderno e responsivo.
- Melhor hierarquia visual com secções de destaque e formulário.
- Inputs, labels, botões e mensagens com estilo consistente.
- Visual alinhado com os padrões usados no formulário de anúncios.

2. Toggle global de tema no cabeçalho
- Botão com ícone dinâmico:
  - meia-lua no tema claro;
  - sol no tema escuro.
- Alternância imediata entre tema claro e escuro em todo o site.

3. Persistência de preferência com LocalStorage
- Chave usada: `imociccopn-theme`.
- O tema escolhido fica guardado no navegador.
- Em visitas futuras, o site abre automaticamente no último tema escolhido.

4. Aplicação inicial do tema no carregamento
- Script no `<head>` aplica o tema logo no início.
- Redução do efeito de "flash" de tema incorreto durante o carregamento da página.

5. Compatibilidade com templates existentes
- Foram adicionadas variáveis CSS base para os dois temas.
- Incluídos ajustes para componentes existentes (cards, formulários e elementos de apoio) para melhorar legibilidade em dark mode.

---

## Ficheiros alterados

- `imovel/templates/imovel/login.html`
- `imovel/templates/imovel/registo.html`
- `imovel/templates/imovel/base.html`

---

## Resultado

O sistema passou a ter uma experiência visual mais consistente nas páginas de autenticação e suporte real a modo claro/escuro com preferência persistente entre sessões.
