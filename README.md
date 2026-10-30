# Sistema de Controle de Estoque

Aplicação de console em **Python** integrada ao **Oracle**, que controla **produtos** e **fornecedores**, com relatórios de estoque baixo e de quantidade comprada.

- **Disciplina:** Banco de Dados — 2026/2
- **Professor:** Howard Roatti
- **Grupo:** Lucas Cardoso

## Funcionalidades

| Menu | O que faz |
|---|---|
| Relatórios | 1) quantidade e valor comprado por fornecedor (`GROUP BY`); 2) produtos com estoque baixo (`JOIN`); 3) produtos com seus fornecedores (`JOIN`) |
| Inserir | Escolhe a entidade, pede cada atributo, insere e pergunta se deseja continuar |
| Remover | Lista registros, pede confirmação e, se o fornecedor tiver produtos, avisa e oferece remover os produtos junto |
| Atualizar | Altera todos os campos (Enter mantém o atual) ou um campo à escolha e exibe o registro atualizado |
| Sair | Encerra o programa |

Ao iniciar, a splash screen mostra o nome do sistema, o grupo e a quantidade de registros de cada tabela (`select count(1) total_<tabela> from <tabela>`).

## Modelo de dados

Diagrama em [`docs/diagrama.pdf`](docs/diagrama.pdf) (fonte Mermaid em [`docs/diagrama.mmd`](docs/diagrama.mmd)).

`FORNECEDORES (1) ── fornece ──< (N) PRODUTOS`

## Estrutura

```
.
├── README.md
├── PROMPTS.md
├── requirements.txt
├── .env.example
├── docs/            diagrama.mmd, diagrama.pdf, diagrama.png
├── sql/             01_criar_tabelas.sql, 02_dados_exemplo.sql
└── src/
    ├── main.py
    ├── conexion/    oracle_queries.py
    ├── model/       fornecedor.py, produto.py
    ├── controller/  controller_fornecedor.py, controller_produto.py
    ├── reports/     relatorios.py
    ├── sql/         consultas dos relatórios
    └── utils/       config.py, console.py, splash_screen.py
```

Não há ORM: todas as consultas são montadas como texto e concatenadas com os atributos (textos passam por escape de aspas simples).

## Como executar (Linux, VM LabDatabase)

O projeto roda na VM Ubuntu da disciplina, onde o Oracle (imagem `gvenzl/oracle-xe:21-slim-faststart`) fica no container `database_services-oracle-1`.

1. **Garanta que o Oracle está no ar** (ele pode demorar para ficar *healthy* na primeira vez):

   ```bash
   docker ps
   docker start database_services-oracle-1   # se o container estiver parado (nome mostrado na coluna NAMES do docker ps)
   ```

2. **Descubra o host.** Se o projeto roda dentro da VM, use `localhost`. Se roda fora (com NAT/port forwarding no VirtualBox), use `localhost` com a porta mapeada. Caso contrário, use o IP da VM:

   ```bash
   ip addr    # procure o IP em enp0s3 ou eth0
   ```

3. **Clonar e instalar dependências** (Python 3.9+):

   ```bash
   git clone https://github.com/LucasCardosoBr/Sistema-de-Controle-de-Estoque.git
   cd Sistema-de-Controle-de-Estoque
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   O driver `oracledb` usa o modo *thin*, sem precisar do Oracle Client. Se faltar o `venv`: `sudo apt install python3-venv python3-pip`.

4. **Configurar a conexão:** copie o modelo e preencha. No container da VM, a senha dos usuários administrativos é `oracle` (usuário `system`); se o AVA indicar outro usuário, use-o. O DSN tem o formato `host:1521/serviço` (o serviço costuma ser `XEPDB1`; confirme com o professor).

   ```bash
   cp .env.example .env
   nano .env
   ```

5. **Criar as tabelas:** no DBeaver, conecte no Oracle (host, porta 1521, serviço, usuário e senha), abra `sql/01_criar_tabelas.sql` e execute como **script** (Alt+X). Depois, se quiser dados de teste, execute `sql/02_dados_exemplo.sql`.

6. **Executar**

   ```bash
   python3 src/main.py
   ```

## Solução de problemas

- **"Credenciais do Oracle não configuradas":** falta criar o arquivo `.env`.
- **`ORA-12541` / `DPY-6005`:** host, porta ou serviço do `ORACLE_DSN` estão errados, ou o container está parado (`docker start database_services-oracle-1`).
- **`ORA-00942` (tabela não existe):** rode o script `sql/01_criar_tabelas.sql` com o mesmo usuário do `.env`.
- **`externally-managed-environment` no pip:** use o ambiente virtual (`python3 -m venv .venv`) como no passo 3.

## Vídeo demonstrativo

<!-- Cole aqui o link do vídeo no YouTube -->
