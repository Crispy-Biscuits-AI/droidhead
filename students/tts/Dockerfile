FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates sox && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN curl -L https://github.com/rhasspy/piper/releases/download/v0.0.2/piper_linux_aarch64.tar.gz | tar xz -C /usr/local/bin --strip-components=1 || true
COPY server.py ./server.py
VOLUME ["/models/tts"]
ENV PIPER_MODEL=/models/tts/voice.onnx
EXPOSE 9001
CMD ["python","-m","uvicorn","server:app","--host","0.0.0.0","--port","9001"]
