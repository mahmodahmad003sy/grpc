FROM python:3.11-slim
WORKDIR /app
COPY services/catalog/requirements.txt .
RUN pip install -r requirements.txt
COPY proto /app/proto
RUN python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/book.proto
COPY services/catalog /app/services/catalog
ENV CATALOG_PORT=50051
CMD ["python","/app/services/catalog/server.py"]
