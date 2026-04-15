# 🔍 Análise da Base de Dados - imociccopngrupo1

## ✅ O que está bem

1. **Estrutura relacional** - As foreign keys estão bem configuradas
2. **Tipos de dados** - Maioritariamente apropriados
3. **Primary keys** - Bem definidas
4. **Auto_increment** - Utilizado corretamente em chaves principais numéricas

---

## ⚠️ Potenciais Problemas Encontrados

### 1. **Tabela `proprietario` - SEM auto_increment**
```sql
-- ATUAL (PROBLEMA):
id_proprietario int primary key,

-- RECOMENDADO:
id_proprietario int primary key auto_increment,
```
**Por quê?** Sem auto_increment, você tem que atribuir IDs manualmente, o que é propenso a erros.

---

### 2. **Falta de UNIQUE constraint nos emails**
```sql
-- ATUAL:
email varchar(999) not null,

-- RECOMENDADO:
email varchar(255) not null unique,
```
**Por quê?** Emails devem ser únicos. Dois anunciantes não podem ter o mesmo email.

---

### 3. **Campo `tipo` em `anunciante` sem documentação**
```sql
-- ATUAL:
tipo int not null,

-- RECOMENDADO (com comentário):
tipo int not null,  -- 1=Proprietário, 2=Consultor, 3=Agência
```
**Por quê?** Facilita entender o que significa cada valor.

---

### 4. **Campos VARCHAR muito grandes**
```sql
-- ATUAL:
descricao varchar(9999),
nome varchar(999),

-- RECOMENDADO:
descricao TEXT,        -- Sem limite de caracteres
nome varchar(255),     -- Suficiente para nomes
```
**Por quê?** TEXT é mais apropriado para textos longos, e varchar(999) é desnecessário para nomes.

---

### 5. **Falta de constraints em campos de telefone**
```sql
-- ATUAL:
telefone varchar(999) not null,

-- RECOMENDADO:
telefone varchar(20) not null,  -- Telefones portugueses têm ~9 dígitos
```

---

## ✅ SQL Corrigido e Otimizado

```sql
-- Base de dados
CREATE DATABASE IF NOT EXISTS imociccopngrupo1;
USE imociccopngrupo1;

-- Tabela: Rede de Agências
CREATE TABLE rede (
    id_rede INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_rede)
);

-- Tabela: Agência (vinculada a uma Rede)
CREATE TABLE agencia (
    id_agencia INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    id_rede INT,
    PRIMARY KEY (id_agencia),
    FOREIGN KEY (id_rede) REFERENCES rede(id_rede)
);

-- Tabela: Consultor (vinculado a uma Agência)
CREATE TABLE consultor (
    id_consultor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    id_agencia INT,
    FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia)
);

-- Tabela: Proprietário
CREATE TABLE proprietario (
    id_proprietario INT PRIMARY KEY AUTO_INCREMENT,  -- ✅ CORRIGIDO: Adicionado auto_increment
    nome VARCHAR(255) NOT NULL
);

-- Tabela: Distrito
CREATE TABLE distrito (
    id_distrito VARCHAR(9) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Tabela: Concelho (vinculado a Distrito)
CREATE TABLE concelho (
    id_concelho VARCHAR(9) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    id_distrito VARCHAR(9),
    FOREIGN KEY (id_distrito) REFERENCES distrito(id_distrito)
);

-- Tabela: Freguesia (vinculada a Concelho)
CREATE TABLE freguesia (
    id_freguesia INT PRIMARY KEY AUTO_INCREMENT,
    codigo_freguesia VARCHAR(9),
    nome VARCHAR(255) NOT NULL,
    id_concelho VARCHAR(9),
    FOREIGN KEY (id_concelho) REFERENCES concelho(id_concelho)
);

-- Tabela: Anunciante
CREATE TABLE anunciante (
    id_anunciante INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,  -- ✅ CORRIGIDO: Adicionado UNIQUE
    telefone VARCHAR(20) NOT NULL,        -- ✅ CORRIGIDO: Reduzido tamanho
    tipo INT NOT NULL,                    -- 1=Proprietário, 2=Consultor, 3=Agência
    id_proprietario INT,
    id_consultor INT,
    id_agencia INT,
    FOREIGN KEY (id_proprietario) REFERENCES proprietario(id_proprietario),
    FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia),
    FOREIGN KEY (id_consultor) REFERENCES consultor(id_consultor)
);

-- Tabela: Imóvel
CREATE TABLE imovel (
    id_imovel INT AUTO_INCREMENT PRIMARY KEY,
    morada VARCHAR(255) NOT NULL,
    data_anuncio DATETIME DEFAULT CURRENT_TIMESTAMP,
    preco DECIMAL(12,2) NOT NULL,
    descricao TEXT,                    -- ✅ CORRIGIDO: Mudado para TEXT
    numero_quartos INT UNSIGNED DEFAULT 0,
    numero_wc INT UNSIGNED DEFAULT 0,
    data_construcao DATE,
    area DECIMAL(6,2) NOT NULL,
    id_anunciante INT NOT NULL,
    id_freguesia INT NOT NULL,
    FOREIGN KEY (id_anunciante) REFERENCES anunciante(id_anunciante),
    FOREIGN KEY (id_freguesia) REFERENCES freguesia(id_freguesia)
);
```

---

## 📊 Diagrama de Relações

```
REDE (1)
  ↓
AGÊNCIA (muitos)
  ↓ ↙
CONSULTOR (muitos)

PROPRIETÁRIO (1)
  ↓
ANUNCIANTE (muitos) ← CONSULTOR (opcional)
  ↓                  ← AGÊNCIA (opcional)
  ↓
IMÓVEL (muitos)
  ↓
FREGUESIA
  ↓
CONCELHO
  ↓
DISTRITO
```

---

## 🎯 Próximos Passos

1. ✅ Executar o SQL corrigido na sua BD MySQL
2. ✅ Verificar se conecta corretamente
3. ⏳ Criar os modelos Django (models.py)
4. ⏳ Configurar settings.py com dados da BD

**Quer que continue com a instalação do `mysqlclient` e configuração da conexão?**
