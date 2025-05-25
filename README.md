
# Dev Sandbox

## 📦 Sobre o projeto

Este projeto é um ambiente de desenvolvimento **completo e containerizado** para execução e orquestração de pipelines de dados. Ele integra Airflow, Spark, ClickHouse, MinIO e Metabase, proporcionando uma plataforma robusta para testes, análises e validação de ETLs.

## 🏗️ Arquitetura do ambiente

O ambiente é totalmente baseado em containers Docker, com cada serviço isolado e configurado em arquivos `docker-compose` especializados.

**Componentes:**

- **Airflow 3.0:** Orquestração de pipelines com operadores personalizados para execução com Docker.
- **2 x PostgreSQL:** Banco de dados de backend do Airflow e Metabase.
- **Dataplataform (Spark):**  
  - Integração com Dataflint, Delta Lake, SparkMeasure e PyDeequ para qualidade e performance.  
  - Conexão com ClickHouse e MinIO.  
  - Suporte a DuckDB para análises locais.
- **ClickHouse:** Banco de dados analítico columnar.
- **MinIO:** Armazenamento de objetos S3-compatible.
- **Metabase:** Visualização de dados, com automação de backup de queries e dashboards.
- **Spark History Server:** Monitoramento de jobs Spark.

## 🛠️ Tecnologias e ferramentas

- **Orquestração:** Airflow 3.0 + PostgreSQL  
- **Processamento:** Apache Spark + Delta Lake + Dataflint + SparkMeasure + PyDeequ  
- **Armazenamento:** MinIO + DuckDB + ClickHouse  
- **Visualização:** Metabase  
- **Infraestrutura:** Docker + Docker Compose + Makefile  
- **Automação:** Scripts shell e utilitários Python  

## 📁 Estrutura do projeto

```
.
├── airflow/               # Airflow config, DAGs, plugins, custom operators
├── clickhouse/           # Configurações e scripts de inicialização do ClickHouse
├── dataplataform/        # Spark config, scripts, JARs e testes
├── metabase/             # Backup do banco de dados do Metabase
├── minio/                # Inicialização, scripts e dados do MinIO
├── orchestration/        # docker-compose especializados
├── .env / .env.example   # Variáveis de ambiente
├── makefile              # Automação de comandos
└── README.md             # Este arquivo
```


## 🛠️ Comandos completos (`Makefile`)

### 🔍 Utilitários

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make check-env`            | Verifica se o arquivo `.env` existe                              |
| `make airflow-password`     | Exibe a senha gerada do Airflow (modo standalone)                |

### 🚀 Inicialização

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make up`                   | Sobe **todos os serviços** com build                              |
| `make up-clickhouse`        | Sobe apenas o ClickHouse                                          |
| `make up-airflow`           | Sobe apenas o Airflow                                             |
| `make up-etl-runner`        | Sobe apenas o ETL Runner (Spark)                                  |
| `make up-metabase`          | Sobe apenas o Metabase                                            |
| `make up-minio`             | Sobe apenas o MinIO                                               |
| `make up-spark-history`     | Sobe apenas o Spark History Server                                |

### ⬇️ Parada e Reset

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make down`                 | Derruba **todos os containers** sem remover volumes              |
| `make down-clean`           | Derruba **todos os containers** e **remove volumes**             |
| `make reset`                | Derruba e sobe novamente todos os serviços                       |

### 🧾 Logs

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make logs-airflow`         | Mostra logs do Airflow                                            |
| `make logs-metabase`        | Mostra logs do Metabase                                           |
| `make logs-clickhouse`      | Mostra logs do ClickHouse                                         |
| `make logs-minio-init`      | Mostra logs do processo de inicialização do MinIO                 |

### 🧪 Testes

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make test`                 | Executa teste de ambiente configurado                             |

### 🚀 Setup Completo

| Comando                      | Descrição                                                        |
| --------------------------- | ---------------------------------------------------------------- |
| `make init`                 | Executa configuração completa: `check-env`, `up` e `airflow-password` |

### 💾 Backup e Restauração do Metabase

| Comando                          | Descrição                                                    |
| -------------------------------- | ------------------------------------------------------------ |
| `make backup-metabase-db`        | Realiza backup do banco de dados do Metabase                 |
| `make restore-metabase-db-clean` | Restaura o banco a partir do backup, apagando tudo antes     |

### 🧹 Limpeza

| Comando                          | Descrição                                                    |
| -------------------------------- | ------------------------------------------------------------ |
| `make clean-spark-events`        | Limpa diretórios de eventos do Spark                         |
| `make minio-clean-all`           | Limpa todos os arquivos dos buckets no MinIO                 |
| `make minio-clean-old`           | Limpa arquivos antigos dos buckets no MinIO                  |
| `make minio-clean-prefix`        | Limpa arquivos de um bucket MinIO baseado em prefixo         |



## ⚙️ Configuração

1. **Variáveis de ambiente:**  
   - Copie `.env.example` para `.env`.  
   - Ajuste conforme a necessidade (senhas, portas, etc).

2. **Volumes persistentes:**  
   - Alguns serviços utilizam volumes locais para manter estado (Ex: `minio/data`, `clickhouse/init-sql`).

3. **Dependências:**  
   - Docker  
   - Docker Compose  
   - Make

## 🚀 Como rodar

O ambiente é totalmente gerenciado pelo `Makefile`.  

### **Subir todos os serviços:**

```bash
make up
```

### **Subir serviços específicos:**

- Airflow: `make up-airflow`  
- ClickHouse: `make up-clickhouse`  
- ETL Runner (Spark): `make up-etl-runner`  
- Metabase: `make up-metabase`  
- MinIO: `make up-minio`  
- Spark History Server: `make up-spark-history`

### **Parar todos os serviços:**

```bash
make down
```

### **Parar serviços específicos:**

- Airflow: `make down-airflow`  
- ClickHouse: `make down-clickhouse`  
- ETL Runner: `make down-etl-runner`  
- Metabase: `make down-metabase`  
- MinIO: `make down-minio`  
- Spark History Server: `make down-spark-history`

## 🧹 Manutenção e troubleshooting

### **Limpeza de diretórios:**

- Limpar eventos do Spark:  
  ```bash
  make clean-spark-events
  ```

- Limpar diretórios de saída:  
  ```bash
  make clean-output
  ```

- Limpeza completa:  
  ```bash
  make clean-all
  ```

## 📊 Visualização de dados

- **Metabase:**  
  - Acesse via: `http://localhost:3000`  
  - Banco de dados configurado com PostgreSQL.  
  - Backup automatizado: `metabase_pg_backup.sql`

- **MinIO:**  
  - Acesse via: `http://localhost:9000`  
  - Credenciais configuradas no `.env`.

- **Spark History Server:**  
  - Monitoramento via interface web após subir `make up-spark-history`.

## 🧪 Testes

- Testes e validações de pipelines localizados em `dataplataform/testes`.  
- Scripts de execução de ETL com Spark, validados com:  
  - **SparkMeasure** para performance  
  - **PyDeequ** para qualidade de dados  
- Integração com **ClickHouse** e **MinIO** para testes fim-a-fim.

## ✅ Conclusão

Este ambiente provê uma infraestrutura robusta para desenvolvimento, testes e validação de pipelines de dados em um ecossistema completo. Use os comandos `make` para gerenciar os serviços de forma eficiente.
