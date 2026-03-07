GET_USER_BY_EMAIL = """
SELECT id, password_hash, role FROM users WHERE email = %s;
"""