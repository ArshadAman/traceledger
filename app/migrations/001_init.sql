CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users Table
CREATE TABLE IF NOT EXISTS users(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN('user', 'admin')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Audit events TABLE
CREATE TABLE IF NOT EXISTS audit_events(
    id UUID NOT NULL, 
    actor_id UUID NOT NULL,
    actor_type TEXT NOT NULL CHECK(actor_type IN ('users', 'system')),
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    resource_id UUID,
    
    status TEXT NOT NULL CHECK (status IN ('success', 'failure')),
    
    metadata JSONB,
    ip_addresss INET,
    
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_actor
        FOREIGN KEY (actor_id)
        REFERENCES users(id)
        ON DELETE CASCADE
)