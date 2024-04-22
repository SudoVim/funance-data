import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

CONFIG_VALUES = {
    "elasticsearch.url": os.getenv("ELASTICSEARCH_URL") or "http://localhost:9200",
    "elasticsearch.username": os.getenv("ELASTICSEARCH_USERNAME") or "elastic",
    "elasticsearch.password": os.getenv("ELASTICSEARCH_PASSWORD") or "",
    "elasticsearch.index_prefix": os.getenv("ELASTICSEARCH_INDEX_PREFIX") or "",
}


def config(key: str) -> Optional[str]:
    """
    Get configuration value denoted by the given ``key``.
    """
    return CONFIG_VALUES[key]
