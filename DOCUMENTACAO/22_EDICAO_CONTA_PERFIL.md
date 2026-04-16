# Passo 22: Página de edição de conta (dados + segurança)

## Objetivo
Permitir que o utilizador edite os seus dados pessoais numa página dedicada e moderna, incluindo atualização de palavra-passe e opções úteis de perfil.

---

## O que foi implementado

1. Nova página de conta
- Nova página acessível por botão na área de cliente.
- Layout moderno e responsivo, coerente com as restantes páginas do portal.
- Estrutura em dois blocos:
  - Dados pessoais;
  - Segurança (alteração de palavra-passe).

2. Edição de dados pessoais
- Campos editáveis:
  - nome de utilizador;
  - primeiro nome;
  - último nome;
  - email;
  - telefone.
- Campo adicional relevante:
  - preferência para receber notificações por email.
- Validações aplicadas:
  - nome de utilizador único;
  - email único;
  - telefone com 9 dígitos.

3. Alteração de palavra-passe
- Formulário dedicado para alterar palavra-passe.
- Mantém sessão ativa após alteração (evita logout automático imediato).

4. Sincronização com entidade anunciante
- Quando aplicável, a atualização de email/telefone do utilizador também sincroniza os dados na tabela de anunciante.

5. Acesso rápido na dashboard
- Botão "Editar conta" adicionado:
  - na área pessoal de utilizador comum;
  - no painel de anunciante.

6. Extensão do perfil de utilizador
- Novos campos no `PerfilUtilizador`:
  - `telefone`;
  - `receber_notificacoes_email`.
- Migração criada e aplicada para suportar os novos campos.

---

## Ficheiros alterados

- `imovel/models.py`
- `imovel/forms.py`
- `imovel/views.py`
- `imovel/urls.py`
- `imovel/admin.py`
- `imovel/templates/imovel/editar_conta.html`
- `imovel/templates/imovel/perfil.html`
- `imovel/templates/imovel/painel_anunciante.html`
- `imovel/migrations/0007_perfilutilizador_receber_notificacoes_email_and_more.py`

---

## Resultado

A aplicação passou a oferecer gestão de conta mais completa e profissional, com atualização de dados críticos e segurança, mantendo consistência visual e integração com o restante domínio imobiliário.
