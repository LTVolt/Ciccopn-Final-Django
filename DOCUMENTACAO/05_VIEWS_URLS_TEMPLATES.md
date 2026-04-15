# Passo 5: Views, URLs e Templates iniciais

## O que foi feito

1. Migrações da app criadas e sincronizadas com a base existente.
2. Views iniciais implementadas para página inicial, lista e detalhe de imóvel.
3. Rotas (URLs) da app configuradas e incluídas no projeto.
4. Templates HTML iniciais criados para navegação e visualização de dados.

---

## 1) Migrações

Comandos executados:
- `python manage.py makemigrations imovel`
- `python manage.py migrate --fake-initial`

Resultado:
- A migração `imovel.0001_initial` foi marcada como `FAKED`, porque as tabelas já existiam no MySQL.
- Isto mantém o histórico de migrações do Django sem recriar tabelas existentes.

---

## 2) Views criadas

Arquivo: [imovel/views.py](../imovel/views.py)

Views:
- `home()`
  - Mostra uma página inicial com o total de imóveis.
- `lista_imoveis()`
  - Carrega e lista todos os imóveis por data mais recente.
- `detalhe_imovel(id_imovel)`
  - Mostra os detalhes de um imóvel específico.

---

## 3) URLs criadas

Arquivos:
- [imovel/urls.py](../imovel/urls.py)
- [config/urls.py](../config/urls.py)

Rotas disponíveis:
- `/` → página inicial
- `/imoveis/` → lista de imóveis
- `/imoveis/<id>/` → detalhe de um imóvel
- `/admin/` → painel administrativo

---

## 4) Templates criados

Arquivos:
- [imovel/templates/imovel/base.html](../imovel/templates/imovel/base.html)
- [imovel/templates/imovel/home.html](../imovel/templates/imovel/home.html)
- [imovel/templates/imovel/lista_imoveis.html](../imovel/templates/imovel/lista_imoveis.html)
- [imovel/templates/imovel/detalhe_imovel.html](../imovel/templates/imovel/detalhe_imovel.html)

Objetivo de cada template:
- `base.html`: layout comum e navegação.
- `home.html`: mensagem inicial e botão para a lista.
- `lista_imoveis.html`: cards com resumo de cada imóvel.
- `detalhe_imovel.html`: informação completa do imóvel.

---

## 5) Validação

Comando executado:
- `python manage.py check`

Resultado:
- Sem erros de configuração.

---

## Próximo passo recomendado

Criar o primeiro utilizador admin e testar no browser:
1. `python manage.py createsuperuser`
2. `python manage.py runserver`
3. Abrir `/admin/`, `/` e `/imoveis/`
