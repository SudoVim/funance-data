import os
import threading
import elasticsearch
from dotenv import load_dotenv

load_dotenv()

app_local = threading.local()


def create_new_client(hostname: str, username: str, password: str):
    """
    Create a new elasticsearch client with the given arguments.
    """
    return elasticsearch.Elasticsearch(
        [hostname],
        http_auth=(
            username,
            password,
        ),
    )


def get_client():
    """
    connect and return the elasticsearch client object
    """
    if not hasattr(app_local, "global_elastic_client"):
        app_local.global_elastic_client = create_new_client(
            os.getenv("ELASTICSEARCH_URL") or "http://localhost:9200",
            os.getenv("ELASTICSEARCH_USERNAME") or "elastic",
            os.getenv("ELASTICSEARCH_PASSWORD") or "",
        )

    return app_local.global_elastic_client
