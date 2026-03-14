BEGIN;
    ALTER TABLE audit_events
    ALTER COLUMN id SET DEFAULT gen_random_uuid();
    
    ALTER TABLE audit_events
    ALTER COLUMN actor_id DROP NOT NULL;
    
    ALTER TABLE audit_events
    DROP CONSTRAINT IF EXISTS audit_events_actor_type_check;
    
    ALTER TABLE audit_events
    ADD CONSTRAINT audit_events_actor_type_check
    CHECK (actor_type IN ('user', 'system'));
    
COMMIT;