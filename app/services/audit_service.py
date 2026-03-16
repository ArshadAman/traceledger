from search.client import es
from search.service import search_cb

def es_search(q: str, start=None, end=None, limit: int = 10, offset: int = 0) -> dict:
    query = {
        "bool":{
            "must": [
                {
                    "match":{
                        "message": q
                    }
                }
            ],
            "filter": []
        }
    }
    # Add filter if start and end are present
    if start and end:
        query["bool"]["filter"].append(
            {
                "range":{
                    "timestamp":{
                        "gte": start, 
                        "lte": end
                    }
                }
            }
        )
    def execute_search():
        return es.search(
            index = "audit_events",
            query=query,
            from_ = offset,
            size = limit,
            sort=[{"timestamp": "desc"}],
            timeout="2s"
        )
    result = search_cb.call(execute_search)
    hits = result["hits"]["hits"]
    total = result["hits"]["total"]["value"]
    items = [h["_source"] for h in hits]
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": items,
    }