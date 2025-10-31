import grpc, time, os
from concurrent import futures
from google.protobuf.json_format import ParseDict
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "proto"))

import book_pb2 as bookpb
import book_pb2_grpc as booksvc
import models

PORT = os.getenv("CATALOG_PORT", "50051")


class CatalogService(booksvc.BookCatalogServicer):
    def AddBook(self, request, context):
        b = request.book
        models.add_book(
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "genres": list(b.genres),
                "rating": b.rating,
            }
        )
        return bookpb.AddBookResponse(book=b)

    def GetBook(self, request, context):
        d = models.get_book(request.id)
        if not d:
            context.abort(grpc.StatusCode.NOT_FOUND, "book not found")
        return bookpb.GetBookResponse(book=ParseDict(d, bookpb.Book()))

    def ListBooks(self, request, context):
        items = [ParseDict(d, bookpb.Book()) for d in models.list_books()]
        return bookpb.ListBooksResponse(books=items)

    def SearchBooks(self, request, context):
        items = [ParseDict(d, bookpb.Book()) for d in models.search(request.query)]
        return bookpb.SearchBooksResponse(books=items)


def serve():
    models.init()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booksvc.add_BookCatalogServicer_to_server(CatalogService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"catalog listening on {PORT}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
