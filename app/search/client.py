from elasticsearch import Elasticsearch

from core.config import settings

es = Elasticsearch(settings.elastic_search_host)

INDEX_NAME = "audit_events"

def index_audit_event(document: dict):
    """
    Sends audit event document to ElasticSearch
    ElasticSerach will store it inside the 'audit_events' index
    """
    es.index(
        index=INDEX_NAME,
        document=document
    )