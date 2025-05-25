.PHONY: clean-spark-events clean-output clean-all

COMPOSE_FILES = \
	-f orchestration/docker-compose.airflow.yml \
	-f orchestration/docker-compose.clickhouse.yml \
	-f orchestration/docker-compose.metabase.yml \
	-f orchestration/docker-compose.spark-history.yml \
	-f orchestration/docker-compose.etl-runner.yml \
	-f orchestration/docker-compose.minio.yml 

# Nome do container do Airflow
AIRFLOW_CONTAINER=airflow
METABASE_CONTAINER=metabase
CLICKHOUSE_CONTAINER=clickhouse


SCRIPTS_DIR=./minIo/scripts

# Nome do container do Postgres usado pelo Metabase
POSTGRES_METABASE_CONTAINER=postgres_metabase
POSTGRES_METABASE_DB=metabase_db
POSTGRES_METABASE_USER=metabase
BACKUP_FILE=metabase/metabase_pg_backup.sql
# Arquivo de variáveis
ENV_FILE=.env

# 🔍 Verifica se o .env existe
check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "⚠️  $(ENV_FILE) não encontrado. Execute: cp .env.example .env"; \
		exit 1; \
	fi

# 🔐 Exibe a senha gerada do Airflow (modo standalone)
airflow-password: check-env
	@echo "🔐 Buscando senha do Airflow..."
	@docker logs $(AIRFLOW_CONTAINER) 2>&1 | grep "Password for user" || echo "⚠️  Container não encontrado ou senha ainda não gerada."


# 🚀 Sobe todos os serviços com build
up: check-env
	@echo "🚀 Subindo todos os containers..."
	docker-compose --env-file $(ENV_FILE) $(COMPOSE_FILES) up -d --build

# ⬇️ Derruba containers sem remover volumes
down:
	@echo "📦 Parando containers..."
	docker-compose --env-file $(ENV_FILE) $(COMPOSE_FILES) down

# 🧼 Derruba tudo e remove volumes
down-clean:
	@echo "🧨 Removendo containers e volumes..."
	docker-compose --env-file $(ENV_FILE) $(COMPOSE_FILES) down -v

# 🔁 Derruba e sobe novamente
reset: down up

# 🧾 Logs do Airflow
logs-airflow:
	@echo "📄 Acompanhando logs do Airflow..."
	docker logs -f $(AIRFLOW_CONTAINER)

# 🧾 Logs do Airflow
logs-metabase:
	@echo "📄 Acompanhando logs do Airflow..."
	docker logs -f $(METABASE_CONTAINER)

logs-clickhouse:
	@echo "📄 Acompanhando logs do clickhouse..."
	docker logs -f $(CLICKHOUSE_CONTAINER)
# 🧪 Teste (placeholder)

logs-minio-init:
	docker logs -f minio-init

test:
	@echo "✅ Teste OK - ambiente configurado"

# 🚀 Setup completo
init: check-env up airflow-password
	@echo "✅ Setup finalizado! Acesse: http://localhost:8080"

up-clickhouse:
	@echo "🚀 Subindo ClickHouse..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.clickhouse.yml up -d --build

up-airflow:
	@echo "🚀 Subindo Airflow..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.airflow.yml up -d --build

up-etl-runner:
	@echo "🚀 Subindo ETL Runner..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.etl-runner.yml up -d --build

up-metabase:
	@echo "🚀 Subindo Metabase..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.metabase.yml up -d --build

up-minio:
	@echo "🚀 Subindo MiniIo..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.minio.yml up -d --build

up-spark-history:
	@echo "🚀 Subindo Spark History..."
	docker-compose --env-file $(ENV_FILE) -f orchestration/docker-compose.spark-history.yml up -d --build


# Faz backup do banco do Metabase
backup-metabase-db:
	@echo "💾 Fazendo backup do banco do Metabase..."
	docker exec -t $(POSTGRES_METABASE_CONTAINER) pg_dump -U $(POSTGRES_METABASE_USER) $(POSTGRES_METABASE_DB) > $(BACKUP_FILE)

# Restaura o banco a partir do backup (apaga tudo antes!)
restore-metabase-db-clean:
	@echo "♻️ Restaurando banco do Metabase (apagando tudo antes)..."
	docker exec -i $(POSTGRES_METABASE_CONTAINER) psql -U $(POSTGRES_METABASE_USER) -d $(POSTGRES_METABASE_DB) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker exec -i $(POSTGRES_METABASE_CONTAINER) psql -U $(POSTGRES_METABASE_USER) -d $(POSTGRES_METABASE_DB) < $(BACKUP_FILE)


# Limpa logs de execução do Spark
clean-spark-events:
	@if [ -d "minIo/staging/spark-events" ]; then \
		echo "🧹 Limpando spark-events..."; \
		rm -rf minIo/staging/spark-events/*; \
		echo "✅ spark-events limpo."; \
	else \
		echo "⚠️ Diretório spark-events não encontrado. Nenhuma ação realizada."; \
	fi

# Limpa diretório de output dos dados processados

.PHONY: clean-all clean-old clean-prefix

# Caminho padrão para os scripts

minio-clean-all:
	@echo "🔴 Limpando todos os arquivos dos buckets no MinIO..."
	@$(SCRIPTS_DIR)/clean_minio_all.sh
	@echo "✅ Limpeza completa concluída."

minio-clean-old:
	@echo "🟠 Limpando arquivos antigos dos buckets no MinIO..."
	@$(SCRIPTS_DIR)/clean_minio_old.sh
	@echo "✅ Limpeza de arquivos antigos concluída."

minio-clean-prefix:
	@echo "🟡 Limpando arquivos por prefixo no MinIO..."
	@$(SCRIPTS_DIR)/clean_minio_prefix.sh
	@echo "✅ Limpeza seletiva concluída."