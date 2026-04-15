# 📚 Passo 3: Criar os Modelos Django

## Objetivo
Transformar as tabelas MySQL em modelos Django que representam os dados do site imobiliário.

---

## O que é um Modelo?

Um **modelo** em Django é uma classe Python que representa uma tabela na base de dados. Quando você cria um modelo, Django automaticamente:
1. ✅ Cria/sincroniza a tabela no MySQL
2. ✅ Cria métodos para buscar, adicionar, editar dados
3. ✅ Valida os dados antes de guardar

---

## Os 9 Modelos Criados

### 1️⃣ **REDE**
```python
class Rede(models.Model):
    id_rede = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
```

**O que representa:** Uma rede/grupo de agências (ex: "Century 21", "Remax")

**Campo por campo:**
- `id_rede` → Identificador único, auto-incrementado
- `nome` → Texto com até 255 caracteres

**Como usar em Python:**
```python
# Criar nova rede
rede = Rede.objects.create(nome="Century 21")

# Buscar todas as redes
todas_redes = Rede.objects.all()

# Buscar uma rede específica
rede = Rede.objects.get(id_rede=1)

# Imprimir
print(rede.nome)  # Output: "Century 21"
```

---

### 2️⃣ **AGÊNCIA**
```python
class Agencia(models.Model):
    id_agencia = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    id_rede = models.ForeignKey(Rede, ...)  # Ligação à Rede
```

**O que representa:** Uma agência imobiliária (ex: "Century 21 - Porto")

**Relação:** Uma agência pertence a uma rede.

**Diagrama:**
```
REDE (1)
  ↓
AGÊNCIA (muitos)
  └─ Century 21 Porto
  └─ Century 21 Lisboa
  └─ Century 21 Braga
```

**Como usar:**
```python
# Criar agência para uma rede
rede = Rede.objects.get(id_rede=1)
agencia = Agencia.objects.create(nome="Porto", id_rede=rede)

# Buscar todas as agências de uma rede
agencias = Agencia.objects.filter(id_rede=rede)

# Acessar a rede da agência
print(agencia.id_rede.nome)  # Output: "Century 21"
```

---

### 3️⃣ **CONSULTOR**
```python
class Consultor(models.Model):
    id_consultor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    id_agencia = models.ForeignKey(Agencia, ...)  # Ligação à Agência
```

**O que representa:** Um agente/consultor imobiliário

**Relação:** Um consultor trabalha numa agência.

**Diagrama:**
```
AGÊNCIA (1)
  ↓
CONSULTOR (muitos)
  └─ João Silva
  └─ Maria Santos
  └─ Pedro Costa
```

---

### 4️⃣ **PROPRIETÁRIO**
```python
class Proprietario(models.Model):
    id_proprietario = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
```

**O que representa:** Alguém que possui um imóvel

**Nota:** Este é um ID manual (não auto_increment), deve ser atribuído manualmente ou sincronizado com outro sistema.

---

### 5️⃣ **DISTRITO**
```python
class Distrito(models.Model):
    id_distrito = models.CharField(max_length=9, primary_key=True)
    nome = models.CharField(max_length=255)
```

**O que representa:** Um distrito português (Porto, Lisboa, Aveiro, etc.)

**Exemplos:**
- id_distrito: "P" → nome: "Porto"
- id_distrito: "L" → nome: "Lisboa"

---

### 6️⃣ **CONCELHO**
```python
class Concelho(models.Model):
    id_concelho = models.CharField(max_length=9, primary_key=True)
    nome = models.CharField(max_length=255)
    id_distrito = models.ForeignKey(Distrito, ...)  # Ligação ao Distrito
```

**O que representa:** Um concelho português

**Relação:** Um concelho pertence a um distrito.

**Diagrama:**
```
DISTRITO (Porto)
  ↓
CONCELHO (muitos)
  └─ Porto
  └─ Matosinhos
  └─ Vila Nova de Gaia
  └─ Maia
```

---

### 7️⃣ **FREGUESIA**
```python
class Freguesia(models.Model):
    id_freguesia = models.AutoField(primary_key=True)
    codigo_freguesia = models.CharField(max_length=9)
    nome = models.CharField(max_length=255)
    id_concelho = models.ForeignKey(Concelho, ...)  # Ligação ao Concelho
```

**O que representa:** Uma freguesia portuguesa

**Relação:** Uma freguesia pertence a um concelho.

**Diagrama:**
```
CONCELHO (Porto)
  ↓
FREGUESIA (muitas)
  └─ Cedofeita
  └─ Massarelos
  └─ Miragaia
  └─ Ribeira
```

---

### 8️⃣ **ANUNCIANTE**
```python
class Anunciante(models.Model):
    TIPO_CHOICES = [
        (1, 'Proprietário'),
        (2, 'Consultor'),
        (3, 'Agência'),
    ]
    
    id_anunciante = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255)
    telefone = models.CharField(max_length=20)
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    
    # Ligações (apenas uma será usada conforme o tipo)
    id_proprietario = models.ForeignKey(Proprietario, ...)
    id_consultor = models.ForeignKey(Consultor, ...)
    id_agencia = models.ForeignKey(Agencia, ...)
```

**O que representa:** Quem anuncia um imóvel

**Tipo de anunciante:**
- `1` = Proprietário individual
- `2` = Consultor de uma agência
- `3` = Agência imobiliária

**Como usar:**
```python
# Criar anunciante do tipo Proprietário
prop = Proprietario.objects.get(id_proprietario=1)
anunciante = Anunciante.objects.create(
    email="joao@email.com",
    telefone="912345678",
    tipo=1,
    id_proprietario=prop
)

# Buscar anunciantes do tipo Consultor
consultores = Anunciante.objects.filter(tipo=2)
```

---

### 9️⃣ **IMÓVEL** (Modelo Principal)
```python
class Imovel(models.Model):
    id_imovel = models.AutoField(primary_key=True)
    morada = models.CharField(max_length=255)
    data_anuncio = models.DateTimeField(auto_now_add=True)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    descricao = models.TextField(null=True, blank=True)
    numero_quartos = models.PositiveIntegerField(default=0)
    numero_wc = models.PositiveIntegerField(default=0)
    data_construcao = models.DateField(null=True, blank=True)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    
    id_anunciante = models.ForeignKey(Anunciante, ...)
    id_freguesia = models.ForeignKey(Freguesia, ...)
```

**O que representa:** Um imóvel à venda/aluguel

**Campos detalhados:**
- `morada` → Endereço completo
- `data_anuncio` → Quando foi publicado (automático)
- `preco` → Preço em euros (ex: 250000.00)
- `descricao` → Texto longo com características
- `numero_quartos` → Quantos quartos (padrão: 0)
- `numero_wc` → Quantas casas de banho (padrão: 0)
- `data_construcao` → Ano/data de construção
- `area` → Área em m² (ex: 150.50)
- `id_anunciante` → Quem está anunciando
- `id_freguesia` → Localização exata

**Métodos especiais:**
```python
# Métodos definidos no modelo
imovel.get_preco_formatado()  # Retorna: "€250,000.00"
imovel.get_localizacao()      # Retorna: "Cedofeita, Porto, Porto"
```

**Como usar:**
```python
# Buscar todos os imóveis
imoveis = Imovel.objects.all()

# Buscar imóveis com 3+ quartos
imoveis_3q = Imovel.objects.filter(numero_quartos__gte=3)

# Buscar imóveis até €300k
imoveis_baratos = Imovel.objects.filter(preco__lte=300000)

# Buscar imóveis de uma freguesia específica
imoveis_cedofeita = Imovel.objects.filter(
    id_freguesia__nome="Cedofeita"
)

# Ordenar por preço (mais caro primeiro)
imoveis = Imovel.objects.order_by('-preco')

# Buscar e imprimir
for imovel in imoveis:
    print(f"{imovel.morada} - {imovel.get_preco_formatado()}")
```

---

## 🔗 Diagrama Completo de Relações

```
REDE (1)
  ↓
  ├─ AGÊNCIA (muitas)
  │   ↓
  │   ├─ CONSULTOR (muitos)
  │   └─ (ligação para ANUNCIANTE)
  │
  └─ (ligação para ANUNCIANTE)

PROPRIETÁRIO (1)
  ↓
  └─ ANUNCIANTE (muitos)
      ├─ tipo=1 (Proprietário)
      ├─ tipo=2 (Consultor)
      └─ tipo=3 (Agência)
      ↓
      └─ IMÓVEL (muitos)
          ↓
          └─ FREGUESIA (muitas)
              ↓
              └─ CONCELHO (muitos)
                  ↓
                  └─ DISTRITO (muitos)
```

---

## ⚙️ Tipos de Campos Django

| Tipo Django | SQL | Exemplo |
|-------------|-----|---------|
| `CharField` | VARCHAR | Nome, morada |
| `TextField` | TEXT | Descrição longa |
| `IntegerField` | INT | Quartos, casas de banho |
| `PositiveIntegerField` | INT (≥0) | Número de quartos |
| `DecimalField(max_digits=12, decimal_places=2)` | DECIMAL | Preço |
| `DateField` | DATE | Data de construção |
| `DateTimeField` | DATETIME | Data e hora |
| `EmailField` | VARCHAR | Email |
| `ForeignKey` | FK | Relação com outro modelo |
| `AutoField` | INT AUTO_INCREMENT | ID automático |

---

## 📋 O que Já Foi Configurado

- ✅ Todos os 9 modelos criados em `imovel/models.py`
- ✅ Admin configurado em `imovel/admin.py` com interfaces de gestão
- ✅ Métodos úteis adicionados (ex: `get_preco_formatado()`)
- ✅ Meta options configuradas (verbose_name, db_table, etc.)

---

## 🎯 Próximas Etapas

1. ⏳ Executar migrações (criar tabelas)
2. ⏳ Criar views (lógica para mostrar dados)
3. ⏳ Criar templates (páginas HTML)
4. ⏳ Configurar URLs (rotas)

**Pronto para prosseguir?**
