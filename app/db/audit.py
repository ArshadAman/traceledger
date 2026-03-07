INSERT_AUDIT_EVENT = """
INSERT INTO audit_events (
    actor_id, actor_type, action, resource, status, metadata
)
VALUES (%s, %s, %s, %s, %s, %s);
"""