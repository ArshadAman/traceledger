GET_USER_BY_EMAIL = """
SELECT id, password_hash, role
FROM users
WHERE email = %s;
"""

CREATE_USER = """
INSERT INTO users (email, password_hash, role)
VALUES (%s, %s, %s)
RETURNING id;
"""