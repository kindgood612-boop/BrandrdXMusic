FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libopus-dev \
    libssl-dev \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# تحديث pip وتثبيت المتطلبات
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --requirement requirements.txt

COPY . .

CMD ["python", "-m", "BrandrdXMusic"]
