# Nome do container do Airflow
AIRFLOW_CONTAINER=dev-sandbox-airflow-standalone-1
METABASE_CONTAINER=dev-sandbox-metabase-1

# Nome do container do Postgres usado pelo Metabase
POSTGRES_METABASE_CONTAINER=dev-sandbox-postgres_metabase-1
POSTGRES_METABASE_DB=metabase_db
POSTGRES_METABASE_USER=metabase
BACKUP_FILE=metabase_pg_backup.sql
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
	@echo "🚀 Subindo containers..."
	docker-compose up -d --build

# 🧼 Derruba tudo e remove volumes
down-clean:
	@echo "🧨 Removendo containers e volumes..."
	docker-compose down -v

# ⬇️ Derruba containers sem remover volumes
down:
	@echo "📦 Parando containers..."
	docker-compose down

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
# 🧪 Teste (placeholder)
test:
	@echo "✅ Teste OK - ambiente configurado"

# 🚀 Setup completo
init: check-env up airflow-password
	@echo "✅ Setup finalizado! Acesse: http://localhost:8080"


# Faz backup do banco do Metabase
backup-metabase-db:
	docker exec -t $(POSTGRES_METABASE_CONTAINER) pg_dump -U $(POSTGRES_METABASE_USER) $(POSTGRES_METABASE_DB) > $(BACKUP_FILE)

# Restaura o banco a partir do backup (apaga tudo antes!)
restore-metabase-db-clean:
	docker exec -i $(POSTGRES_METABASE_CONTAINER) psql -U $(POSTGRES_METABASE_USER) -d $(POSTGRES_METABASE_DB) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker exec -i $(POSTGRES_METABASE_CONTAINER) psql -U $(POSTGRES_METABASE_USER) -d $(POSTGRES_METABASE_DB) < $(BACKUP_FILE)