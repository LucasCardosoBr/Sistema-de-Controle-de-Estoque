select p.id_produto,
       p.nome as produto,
       p.preco_unitario as preco,
       p.quantidade_estoque as estoque,
       p.quantidade_comprada as comprada,
       f.nome as fornecedor,
       f.cnpj
from produtos p
inner join fornecedores f on f.id_fornecedor = p.id_fornecedor
order by f.nome, p.nome
