-- Dados de exemplo (opcional) para testar os relatorios

INSERT INTO fornecedores VALUES (seq_fornecedores.NEXTVAL, 'Distribuidora Alfa', '11.111.111/0001-11', '(27) 3000-1111', 'contato@alfa.com.br');
INSERT INTO fornecedores VALUES (seq_fornecedores.NEXTVAL, 'Papelaria Beta', '22.222.222/0001-22', '(27) 3000-2222', 'vendas@beta.com.br');
INSERT INTO fornecedores VALUES (seq_fornecedores.NEXTVAL, 'Tech Gama', '33.333.333/0001-33', '(27) 3000-3333', 'comercial@gama.com.br');

INSERT INTO produtos VALUES (seq_produtos.NEXTVAL, 'Caneta azul', 2.50, 8, 20, 200, 2);
INSERT INTO produtos VALUES (seq_produtos.NEXTVAL, 'Caderno 100 folhas', 15.90, 45, 15, 80, 2);
INSERT INTO produtos VALUES (seq_produtos.NEXTVAL, 'Mouse USB', 39.90, 3, 10, 30, 3);
INSERT INTO produtos VALUES (seq_produtos.NEXTVAL, 'Teclado ABNT2', 89.90, 12, 5, 25, 3);
INSERT INTO produtos VALUES (seq_produtos.NEXTVAL, 'Resma papel A4', 29.90, 5, 10, 60, 1);

COMMIT;
