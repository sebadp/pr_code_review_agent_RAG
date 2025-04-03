.PHONY: reset ingest dev

REPO_PATH ?= repos/$(GITHUB_USER)_$(REPO_NAME)

reset:
	@echo "🧹 Deleting vectorstore..."
	rm -rf data/vectorstore
	@echo "✅ Vectorstore deleted."

ingest:
	@echo "📥 Ingesting from '$(REPO_PATH)'..."
	python -m app.cognition.ingest_one_repo $(REPO_PATH)

dev: reset ingest
	@echo "🚀 Starting backend..."
	uvicorn chat_api:app --reload
