# 🚀 Dev Sandbox: Stack de Dados Local com Airflow, Spark, DuckDB, Metabase e ClickHouse

## 📦 Visão Geral
Este projeto provisiona um ambiente local completo para workflows de dados:

- **Airflow 3.0**: orquestração de DAGs
- **PostgreSQL (Airflow e Metabase separados)**
- **Spark + DuckDB**: execução de ETLs
- **Metabase**: visualização de dados
- **ClickHouse**: banco analítico

Tudo rodando via `docker-compose`, com configurações em `.env` e automações via `Makefile`.

---

## ⚙️ Requisitos

- Docker
- Docker Compose v2+
- GNU Make (já incluso no macOS/Linux)

---

## 🧪 Primeiros passos

```bash
make init        # Prepara tudo (env, builda e sobe os containers)
make up          # Sobe todos os containers
make airflow-password  # Exibe a senha gerada do Airflow (modo standalone)
```

---

## 📂 Estrutura

```text
.
├── dags/                       # DAGs do Airflow
├── etl/                        # Scripts ETL (Spark, DuckDB)
├── docker/
│   └── airflow/Dockerfile      # Airflow com dependências extras
│   └── etl-runner/Dockerfile   # etl-runner
├── .env.example                # Exemplo de variáveis do projeto
├── docker-compose.yml          # Stack completo
├── Makefile                    # Comandos automatizados
└── README.md                   # Este arquivo
```

---

## 🌐 URLs principais

| Serviço    | URL                     | Login                         |
|------------|--------------------------|-------------------------------|
| Airflow    | http://localhost:8080    | `admin` / gerado no log       |
| Metabase   | http://localhost:3000    | Setup via UI                  |
| ClickHouse | http://localhost:8123    | Usuário `default`, sem senha  |
| History Server | http://localhost:18080   |   |

---

## 🧰 Comandos via `make`

```bash
make init                  # Cria .env se não existir, builda e sobe os containers
make up                    # Sobe todos os serviços com build (docker-compose up -d --build)
make down                  # Derruba os containers (mantém volumes)
make down-clean            # Derruba tudo e remove volumes (docker-compose down -v)
make reset                 # Reinicia os serviços do zero (down + up)
make logs-airflow          # Mostra logs em tempo real do Airflow standalone
make airflow-password      # Exibe a senha gerada automaticamente pelo Airflow (standalone)
make test                  # Executa teste de ambiente
make backup-metabase-db    # Faz backup do banco do Metabase para um arquivo local .sql
make restore-metabase-db-clean # Restaura o banco do Metabase a partir do .sql (drop + restore)
```