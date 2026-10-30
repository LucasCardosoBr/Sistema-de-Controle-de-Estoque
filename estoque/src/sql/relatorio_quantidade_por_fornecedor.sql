select f.nome as fornecedor,
       count(p.id_produto) as total_produtos,
       nvl(sum(p.quantidade_comprada), 0) as qtd_comprada,
       nvl(sum(p.quantidade_comprada * p.preco_unitario), 0) as valor_comprado
from fornecedores f
left join produtos p on p.id_fornecedor = f.id_fornecedor
group by f.id_fornecedor, f.nome
order by qtd_comprada desc
