import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

CONFIG_VALUES = {
    "elasticsearch": {
        "url": os.getenv("ELASTICSEARCH_URL") or "http://localhost:9200",
        "username": os.getenv("ELASTICSEARCH_USERNAME") or "elastic",
        "password": os.getenv("ELASTICSEARCH_PASSWORD") or "",
        "index_prefix": os.getenv("ELASTICSEARCH_INDEX_PREFIX") or "",
    },
}


def config(key: str) -> Optional[str]:
    """
    Get configuration value denoted by the given ``key``.
    """
    parts = key.split(".")
    c = CONFIG_VALUES
    for part in parts:
        if part not in c:
            return None

        c = c[part]

    return c
