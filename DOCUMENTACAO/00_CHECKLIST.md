# ✅ Checklist de Progresso - Site Imobiliário Django

## Fase 1: Setup ✅ COMPLETO
- [x] Python 3.14.3 instalado
- [x] Django 5.2.13 instalado
- [x] Projeto Django criado (`config`)
- [x] Aplicação `imovel` criada
- [x] App adicionada a `INSTALLED_APPS`
- [x] Documentação inicial criada

---

## Fase 2: Base de Dados (✅ COMPLETO)
- [x] Informação da BD MySQL recolhida
- [x] settings.py configurado com dados MySQL
- [x] Pacote `mysqlclient` instalado
- [x] Conexão preparada

---

## Fase 3: Modelos (✅ COMPLETO)
- [x] Modelos criados em `imovel/models.py` (9 modelos)
- [x] Admin configurado em `imovel/admin.py`
- [x] Métodos utilitários adicionados
- [x] Modelos documentados detalhadamente
- [x] `makemigrations` executado
- [x] `migrate` executado (`--fake-initial`)

---

## Fase 4: Views e URLs (✅ COMPLETO)
- [x] Views criadas em `imovel/views.py`
- [x] URLs configuradas em `imovel/urls.py`
- [x] URLs incluídas em `config/urls.py`
- [x] Documentação de views criada

---

## Fase 5: Templates (✅ COMPLETO)
- [x] Pasta `templates/imovel/` criada
- [x] Template base criado
- [x] Templates para listagem criados
- [x] Templates para detalhe criados

---

## Fase 6: Admin Django (✅ COMPLETO)
- [x] Admin configurado em `admin.py`
- [x] Utilizador admin criado
- [x] Painel testado

---

## Fase 7: Testes e Refinamento (✅ COMPLETO)
- [x] Servidor iniciado com sucesso
- [x] Páginas visualizadas no navegador
- [x] Dados da BD mostrados corretamente

---

## Fase 8: Filtros de Pesquisa (✅ COMPLETO)
- [x] Filtro por Distrito em dropdown
- [x] Filtro por Concelho dependente do Distrito
- [x] Filtro por Freguesia dependente do Concelho
- [x] Filtro por tipologia (0 a 9)
- [x] Filtro por número de WC (0 a 9)
- [x] Filtro por preço mínimo/máximo
- [x] Filtro por área mínima/máxima

---

## Fase 9: Autenticação de Utilizadores (✅ COMPLETO)
- [x] Formulário de registo de conta
- [x] Login de utilizador
- [x] Logout de utilizador
- [x] Área pessoal protegida (`login_required`)
- [x] Mensagens de feedback (login/registo/logout)
- [x] Templates de autenticação criados
- [x] Rotas de autenticação configuradas
- [x] Configuração de redirecionamentos em `settings.py`

---

## Fase 10: Permissões por Papel (✅ COMPLETO)
- [x] Modelo `PerfilUtilizador` criado
- [x] Tipos de conta: Comum e Anunciante
- [x] Escolha do tipo de conta no registo
- [x] Criação automática do perfil no login/registo
- [x] Área pessoal adaptada por papel
- [x] Painel exclusivo para anunciante
- [x] Bloqueio de acesso a painel de anunciante para conta comum
- [x] Perfil de utilizador registado no admin

---

## Fase 12: Registo Aprimorado para Anunciantes (✅ COMPLETO)
- [x] Campos adicionais no registo: primeiro nome, último nome, telefone
- [x] Validação de telefone (9 dígitos, prefixo +351 automático)
- [x] Campo tipo de anunciante (dropdown) apenas para contas de anunciante
- [x] JavaScript para mostrar/esconder campo tipo de anunciante
- [x] Criação automática de Anunciante na BD ao registar
- [x] Criação de Proprietario/Consultor/Agencia conforme tipo
- [x] Validação obrigatória do tipo de anunciante para anunciantes
- [x] Template de registo atualizado com campos individuais

---

**Próxima Ação:**
Implementação concluída: eliminação de anúncios com confirmação e upload de imagens do imóvel.

---

## Fase 13: Eliminação e Upload de Imagens (✅ COMPLETO)
- [x] Eliminação de anúncios com confirmação segura
- [x] Utilizador deve escrever “apagar” para confirmar
- [x] Upload de imagem principal para anúncio
- [x] Templates de criação/edição aceitam ficheiros
- [x] Configuração de MEDIA_URL e MEDIA_ROOT
- [x] Servir imagens em desenvolvimento com Django
- [x] Admin atualizado para mostrar imagem
