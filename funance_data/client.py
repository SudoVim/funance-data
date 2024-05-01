import threading
import elasticsearch

from funance_data.config import config

app_local = threading.local()


def create_new_client(hostname: str, username: str, password: str):
    """
    Create a new elasticsearch client with the given arguments.
    """
    return elasticsearch.Elasticsearch(
        [hostname],
        basic_auth=(
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
            config("elasticsearch.url"),
            config("elasticsearch.username"),
            config("elasticsearch.password"),
        )

    return app_local.global_elastic_client
