FROM python:3.10-slim-bullseye

# تحديث وتثبيت Git و FFmpeg في خطوة واحدة لتقليل حجم الصورة
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# تجهيز مجلد العمل
WORKDIR /app/

# نسخ ملف المتطلبات فقط الأول (عشان السرعة)
COPY requirements.txt .

# تحديث pip وتثبيت المتطلبات
RUN python3 -m pip install --upgrade pip setuptools \
    && pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# دلوقتي ننسخ باقي ملفات البوت
COPY . .

# أمر التشغيل
CMD ["python3", "-m", "BrandrdXMusic"]
