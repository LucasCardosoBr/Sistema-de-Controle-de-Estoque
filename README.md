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

## Como executar (Linux)

1. **Pré-requisitos:** Python 3.9+ e acesso ao Oracle da VM da disciplina.

   ```bash
   python3 --version
   ```

2. **Clonar e instalar dependências**

   ```bash
   git clone https://github.com/LucasCardosoBr/Sistema-de-Controle-de-Estoque/tree/main
   cd <repositorio>
   pip install -r requirements.txt
   ```

   O driver `oracledb` usa o modo *thin*, sem precisar do Oracle Client.

3. **Configurar a conexão:** copie o modelo e preencha usuário, senha e DSN (`host:porta/serviço`).

   ```bash
   cp .env.example .env
   nano .env
   ```

4. **Criar as tabelas:** execute `sql/01_criar_tabelas.sql` no SQL Developer ou no sqlplus. Opcionalmente, rode `sql/02_dados_exemplo.sql` para carregar dados de teste.

   ```bash
   sqlplus usuario/senha@//localhost:1521/XEPDB1 @sql/01_criar_tabelas.sql
   sqlplus usuario/senha@//localhost:1521/XEPDB1 @sql/02_dados_exemplo.sql
   ```

5. **Executar**

   ```bash
   python3 src/main.py
   ```

## Solução de problemas

- **"Credenciais do Oracle não configuradas":** falta criar o arquivo `.env`.
- **`ORA-12541` / `DPY-6005`:** host, porta ou serviço do `ORACLE_DSN` estão errados, ou o listener está parado.
- **`ORA-00942` (tabela não existe):** rode o script `sql/01_criar_tabelas.sql` com o mesmo usuário do `.env`.

## Vídeo demonstrativo

<!-- Cole aqui o link do vídeo no YouTube -->
