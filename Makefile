.PHONY: reset ingest dev

REPO_PATH ?= repos/$(GITHUB_USER)_$(REPO_NAME)

reset_db:
	@echo "🧹 Deleting vectorstore..."
	rm -rf data/vectorstore
	@echo "✅ Vectorstore deleted."

ingest:
	@echo "📥 Ingesting from '$(REPO_PATH)'..."
	python -m app.services.vectorstore.ingest_db_scripts.ingest_one_repo $(REPO_PATH)

run:
	@echo "🚀 Starting backend..."
	uvicorn uvicorn app.api.main:app --reload
