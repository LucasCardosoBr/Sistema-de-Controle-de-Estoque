select p.id_produto,
       p.nome as produto,
       p.quantidade_estoque as estoque,
       p.estoque_minimo as minimo,
       (p.estoque_minimo - p.quantidade_estoque) as faltam,
       f.nome as fornecedor,
       f.telefone
from produtos p
inner join fornecedores f on f.id_fornecedor = p.id_fornecedor
where p.quantidade_estoque <= p.estoque_minimo
order by faltam desc, p.nome
