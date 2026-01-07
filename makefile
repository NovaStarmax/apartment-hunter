.PHONY: run-back run-front dev

run-back:
	uv run uvicorn backend.api:app --reload --port 8000

run-front:
	uv run streamlit run frontend/index.py

dev:
	make -j2 run-back run-front