import grpc, os
import book_pb2 as bookpb
import book_pb2_grpc as booksvc

CAT_ADDR = os.getenv("CATALOG_ADDR", "catalog:50051")


class CatalogClient:
    def __init__(self):
        self.chan = grpc.insecure_channel(CAT_ADDR)
        self.stub = booksvc.BookCatalogStub(self.chan)

    def list_books(self):
        return self.stub.ListBooks(bookpb.ListBooksRequest()).books

    def get_book(self, id_):
        return self.stub.GetBook(bookpb.GetBookRequest(id=id_)).book

    def search(self, q):
        return self.stub.SearchBooks(bookpb.SearchBooksRequest(query=q)).books
