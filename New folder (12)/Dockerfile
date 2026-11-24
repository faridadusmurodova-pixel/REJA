# 39. DOCKERFILE
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ilova

# Tizim paketlari
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Python talablari
COPY talablar.txt /ilova/
RUN pip install --no-cache-dir -r talablar.txt

# Loyiha kodlari
COPY . /ilova/

# Statik fayllarni yig'ish va port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
