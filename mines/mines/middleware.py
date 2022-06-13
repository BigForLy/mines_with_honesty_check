import time
from django.db import connection, reset_queries


class CountQueryMiddleware:
    def __init__(self, response) -> None:
        self.get_response = response

    def __call__(self, request):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()

        response = self.get_response(request)

        end = time.perf_counter()
        end_queries = len(connection.queries)
        print(connection.queries, end='\n')
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")

        return response
