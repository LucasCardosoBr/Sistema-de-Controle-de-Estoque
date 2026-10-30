-- Sistema de Controle de Estoque - Oracle
-- Execute com o usuario do banco da disciplina (SQL Developer ou sqlplus).

-- Limpeza (ignora erro se os objetos ainda nao existem)
BEGIN EXECUTE IMMEDIATE 'DROP TABLE produtos CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE fornecedores CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_fornecedores'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_produtos'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

CREATE SEQUENCE seq_fornecedores START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_produtos     START WITH 1 INCREMENT BY 1 NOCACHE;

CREATE TABLE fornecedores (
    id_fornecedor  NUMBER(10)    NOT NULL,
    nome           VARCHAR2(100) NOT NULL,
    cnpj           VARCHAR2(18)  NOT NULL,
    telefone       VARCHAR2(20),
    email          VARCHAR2(100),
    CONSTRAINT pk_fornecedores PRIMARY KEY (id_fornecedor),
    CONSTRAINT uq_fornecedores_cnpj UNIQUE (cnpj)
);

CREATE TABLE produtos (
    id_produto          NUMBER(10)    NOT NULL,
    nome                VARCHAR2(100) NOT NULL,
    preco_unitario      NUMBER(10,2)  NOT NULL,
    quantidade_estoque  NUMBER(10)    NOT NULL,
    estoque_minimo      NUMBER(10)    NOT NULL,
    quantidade_comprada NUMBER(10)    DEFAULT 0 NOT NULL,
    id_fornecedor       NUMBER(10)    NOT NULL,
    CONSTRAINT pk_produtos PRIMARY KEY (id_produto),
    CONSTRAINT fk_produtos_fornecedor FOREIGN KEY (id_fornecedor)
        REFERENCES fornecedores (id_fornecedor),
    CONSTRAINT ck_produtos_preco   CHECK (preco_unitario >= 0),
    CONSTRAINT ck_produtos_estoque CHECK (quantidade_estoque >= 0),
    CONSTRAINT ck_produtos_minimo  CHECK (estoque_minimo >= 0),
    CONSTRAINT ck_produtos_comprada CHECK (quantidade_comprada >= 0)
);

CREATE INDEX ix_produtos_fornecedor ON produtos (id_fornecedor);
