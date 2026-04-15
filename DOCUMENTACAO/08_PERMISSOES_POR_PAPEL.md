# Passo 8: Permissões por papel (Comum vs Anunciante)

## Objetivo
Separar funcionalidades por tipo de utilizador:
- Conta comum
- Conta anunciante

---

## Implementação realizada

### 1) Novo modelo de perfil de utilizador
Arquivo: [imovel/models.py](../imovel/models.py)

Foi criado o modelo `PerfilUtilizador` com:
- Ligação `OneToOne` ao utilizador Django (`User`)
- Campo `tipo_utilizador` com opções:
  - `COMUM`
  - `ANUNCIANTE`

Tabela nova na BD:
- `perfil_utilizador`

Migração criada e aplicada:
- `imovel/migrations/0002_perfilutilizador.py`

---

### 2) Registo com escolha de tipo de conta
Arquivo: [imovel/forms.py](../imovel/forms.py)

No `RegistoForm` foi adicionado:
- Campo `tipo_utilizador` (dropdown)

No `registo()`:
- Conta é criada
- Perfil é criado/atualizado com o tipo escolhido
- Redireciona para:
  - Painel anunciante (se for anunciante)
  - Área pessoal (se for comum)

---

### 3) Regras de permissão nas views
Arquivo: [imovel/views.py](../imovel/views.py)

Adições:
- `_get_or_create_perfil(user)`
- `painel_anunciante()` com `@login_required`

Regra de acesso ao painel:
- Permitido se perfil for anunciante ou superuser
- Negado para conta comum (com mensagem)

---

### 4) Novas rotas
Arquivo: [imovel/urls.py](../imovel/urls.py)

Rota adicionada:
- `/conta/anunciante/`

---

### 5) Interface adaptada por papel
Arquivos:
- [imovel/templates/imovel/perfil.html](../imovel/templates/imovel/perfil.html)
- [imovel/templates/imovel/painel_anunciante.html](../imovel/templates/imovel/painel_anunciante.html)
- [imovel/templates/imovel/registo.html](../imovel/templates/imovel/registo.html)

Comportamento:
- Conta comum: vê informações básicas da área pessoal
- Conta anunciante: vê estatísticas e lista de imóveis associados ao email
- Painel anunciante mostra imóveis do anunciante

---

## Como testar

1. Criar conta comum em `/conta/registo/`
   - Confirmar acesso à área pessoal
   - Tentar `/conta/anunciante/` e validar bloqueio

2. Criar conta anunciante em `/conta/registo/`
   - Confirmar redirecionamento para `/conta/anunciante/`
   - Confirmar listagem dos imóveis associados ao email

3. No admin, verificar perfis:
   - `/admin/` > Perfis de Utilizador

---

## Resultado
O sistema já separa utilizadores comuns e anunciantes, com comportamento e permissões diferentes, mantendo a estrutura evolutiva para o próximo passo (criação/edição de anúncios por anunciante).
