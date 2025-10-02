FROM nvcr.io/nvidia/l4t-ml:r36.2.0-py3
RUN apt-get update && apt-get install -y --no-install-recommends i2c-tools python3-smbus && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY server.py ./server.py
ENV I2C_BUS=/dev/i2c-1 BATTERY_ADDR=0x36 BATTERY_MONITOR=max17048
EXPOSE 7000
CMD ["python3","-m","uvicorn","server:app","--host","0.0.0.0","--port","7000"]
