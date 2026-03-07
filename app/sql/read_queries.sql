-- select * from users; wrong way to do this
-- Right way is to select the required fields
SELECT id, email, role, created_at
FROM users;

SELECT id, email, role
FROM users
WHERE id = '3212f726-13df-4bd5-9726-e0aad3b78013';


SELECT id, password_hash, role
FROM users
WHERE email = 'arshad@test.com';

-- Sorting (needed to order pages in pagination)
SELECT id, action, status, created_at
FROM audit_events
ORDER BY created_at DESC;

-- Pagination limit, offset (offset = (page - 1) * limit)
SELECT id, action, status, created_at
FROM audit_events
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;

-- FILTER + PAGINATION (REAL API QUERY): GET /users/{id}/audit-events?limit=20&offset=0
-- SELECT id, action, status, created_at
-- FROM audit_events
-- WHERE actor_id = 'USER_UUID'
-- ORDER BY created_at DESC
-- LIMIT 20 OFFSET 0;
-- 
SELECT COUNT(*)
FROM audit_events
WHERE actor_id = 'db7e097a-87e3-401f-86ea-5ebb0e1509fd';


SELECT id, action
FROM audit_events
WHERE metadata->>'method' = 'password';