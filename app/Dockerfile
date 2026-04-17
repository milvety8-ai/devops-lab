# app/Dockerfile
FROM python:3.12-slim
# Метаданные
LABEL maintainer="milvety8@email.com"
LABEL description="DevOps lab application"
# Рабочая директория
WORKDIR /app
# Сначала копируем зависимости (для кэширования слоёв)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Потом копируем код
COPY . .
# Не запускаем от root
RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["python", "app.py"]