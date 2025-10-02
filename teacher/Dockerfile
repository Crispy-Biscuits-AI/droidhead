FROM nvcr.io/nvidia/l4t-ml:r36.2.0-py3
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python3","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
