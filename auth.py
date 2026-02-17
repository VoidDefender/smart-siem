from werkzeug.security import generate_password_hash, check_password_hash
from database import execute_query

def create_user(username, password, role="analyst"):
    password_hash = generate_password_hash(password)

    query = """
    INSERT INTO users (username, password_hash, role)
    VALUES (%s, %s, %s)
    """

    execute_query(query, (username, password_hash, role))


def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username=%s"
    result = execute_query(query, (username,), fetch=True)

    if result:
        user = result[0]
        if check_password_hash(user["password_hash"], password):
            return user

    return None
