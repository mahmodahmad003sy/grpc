import grpc, time, math, os
from concurrent import futures
from google.protobuf.json_format import MessageToDict
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "proto"))

import recommender_pb2 as recpb
import recommender_pb2_grpc as recsvc
import book_pb2 as bookpb
from client_catalog import CatalogClient

PORT = os.getenv("REC_PORT", "50052")


def jaccard(a, b):
    sa, sb = set(a), set(b)
    return len(sa & sb) / (len(sa | sb) or 1)


def score(seed, cand):
    return 0.7 * jaccard(seed.genres, cand.genres) + 0.3 * (cand.rating / 5.0)


class RecommenderService(recsvc.RecommenderServicer):
    def __init__(self):
        self.cat = CatalogClient()

    def Recommend(self, request, context):
        books = list(self.cat.list_books())
        if request.book_id:
            seed = self.cat.get_book(request.book_id)
        else:
            qs = self.cat.search(request.seed_title)
            if not qs:
                context.abort(grpc.StatusCode.NOT_FOUND, "seed not found")
            seed = qs[0]
        ranked = sorted(
            (b for b in books if b.id != seed.id),
            key=lambda b: score(seed, b),
            reverse=True,
        )
        k = request.k if request.k > 0 else 5
        return recpb.RecommendResponse(items=ranked[:k])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recsvc.add_RecommenderServicer_to_server(RecommenderService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"recommender listening on {PORT}", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
