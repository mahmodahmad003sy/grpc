FROM python:3.11-slim
WORKDIR /app
COPY services/recommender/requirements.txt .
RUN pip install -r requirements.txt
COPY proto /app/proto
RUN python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/book.proto proto/recommender.proto
COPY services/recommender /app/services/recommender
ENV REC_PORT=50052
ENV CATALOG_ADDR=catalog:50051
CMD ["python","/app/services/recommender/server.py"]
