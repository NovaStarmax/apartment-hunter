FROM python:3.11-slim
WORKDIR /app

# deps
COPY frontend/requirements.txt /app/frontend/requirements.txt
RUN pip install --no-cache-dir -r /app/frontend/requirements.txt

COPY frontend /app/frontend

EXPOSE 8501
CMD ["streamlit", "run", "frontend/index.py", "--server.address=0.0.0.0", "--server.port=8501"]