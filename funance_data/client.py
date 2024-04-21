import os
import threading
import elasticsearch
from dotenv import load_dotenv

load_dotenv()

app_local = threading.local()


def elastic_client():
    """
    connect and return the elasticsearch client object
    """
    if not hasattr(app_local, "global_elastic_client"):
        app_local.global_elastic_client = elasticsearch.Elasticsearch(
            [os.getenv("ELASTICSEARCH_URL") or "http://localhost:9200"],
            http_auth=(
                os.getenv("ELASTICSEARCH_USERNAME"),
                os.getenv("ELASTICSEARCH_PASSWORD"),
            ),
        )

    return app_local.global_elastic_client
