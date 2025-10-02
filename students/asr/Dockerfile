FROM nvcr.io/nvidia/l4t-ml:r36.2.0-py3
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY server.py ./server.py
ENV ASR_MODEL_SIZE=small ASR_DEVICE=auto ASR_BEAM_SIZE=1 ASR_COMPUTE_TYPE=auto
EXPOSE 9000
CMD ["python3","-m","uvicorn","server:app","--host","0.0.0.0","--port","9000"]
