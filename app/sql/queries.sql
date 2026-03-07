BEGIN;

WITH new_user AS (
    INSERT INTO users (email, password_hash, role)
    VALUES ('arshad11@test.com', 'hash_here', 'user')
    RETURNING id
)
INSERT INTO audit_events (
    actor_id,
    actor_type,
    action,
    resource,
    resource_id,
    status,
    metadata,
    ip_address
)
SELECT
    id,
    'user',
    'USER_LOGIN',
    'user',
    id,
    'success',
    '{"method":"password"}',
    '127.0.0.1'
FROM new_user;

COMMIT;
SELECT id, email, created_at FROM users;
SELECT actor_id, action, status, created_at FROM audit_events;
INSERT INTO users (email, password_hash, role)
VALUES ('x@y.com', 'hash', 'superadmin');
INSERT INTO audit_events (
  actor_id, actor_type, action, resource, status
)
VALUES (
  gen_random_uuid(),
  'user',
  'LOGIN',
  'user',
  'success'
);