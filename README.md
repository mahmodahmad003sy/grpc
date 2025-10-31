# gRPC

Server IP: 5.53.125.80

Local machine: Windows. Server: Linux.

## Description

Two Python microservices using gRPC and Protocol Buffers:

- Catalog (port 50051): store/manage books
- Recommender (port 50052): recommends similar books via Catalog

## Deploy (Linux)

```bash
git clone https://github.com/mahmodahmad003sy/grpc.git
cd grpc
docker compose -f compose/docker-compose.yml up -d
docker logs --tail 20 -f catalog
```

## Test from Windows (PowerShell)

- Seed default dataset (run first)

```powershell
python -c "import grpc,book_pb2 as b,book_pb2_grpc as s; st=s.BookCatalogStub(grpc.insecure_channel('5.53.125.80:50051')); data=[('1','Dune','Frank Herbert',['sci-fi','classic'],4.7),('2','Neuromancer','William Gibson',['sci-fi','cyberpunk'],4.3),('3','The Hobbit','J.R.R. Tolkien',['fantasy','classic'],4.8),('4','Snow Crash','Neal Stephenson',['sci-fi','cyberpunk'],4.2),('5','The Name of the Wind','Patrick Rothfuss',['fantasy'],4.6)]; [st.AddBook(b.AddBookRequest(book=b.Book(id=i,title=t,author=a,genres=g,rating=r))) for (i,t,a,g,r) in data]; print('seeded')"
```

- List books

```powershell
python -c "import grpc,book_pb2 as b,book_pb2_grpc as s; st=s.BookCatalogStub(grpc.insecure_channel('5.53.125.80:50051')); print(st.ListBooks(b.ListBooksRequest()))"
```

- Add one book

```powershell
python -c "import uuid,grpc,book_pb2 as b,book_pb2_grpc as s; addr='5.53.125.80:50051'; bid=str(uuid.uuid4()); st=s.BookCatalogStub(grpc.insecure_channel(addr)); st.AddBook(b.AddBookRequest(book=b.Book(id=bid,title='Test',author='A',genres=['sci-fi'],rating=4.2))); print(bid)"
```

- Get by id (change the ID each time to your last printed id)

```powershell
python -c "import grpc,book_pb2 as b,book_pb2_grpc as s; addr='5.53.125.80:50051'; bid='PUT_ID_HERE'; st=s.BookCatalogStub(grpc.insecure_channel(addr)); print(st.GetBook(b.GetBookRequest(id=bid)))"
```

- Clear all books, then list

```powershell
python -c "import grpc,book_pb2 as b,book_pb2_grpc as s; addr='5.53.125.80:50051'; st=s.BookCatalogStub(grpc.insecure_channel(addr)); print(st.Clear(b.ClearRequest())); print(st.ListBooks(b.ListBooksRequest()))"
```

## Services

| Service     | Port  | Description                          |
| ----------- | ----- | ------------------------------------ |
| catalog     | 50051 | Book management gRPC API             |
| recommender | 50052 | Recommends similar books via catalog |
