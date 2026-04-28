import sqlite3
from User.Role import RoleBased
from User.User import UserRole

def connect():
    """Return a database connection for the user database."""
    return sqlite3.connect("SDB_User.db")


def create_table():
    """Create the users table if it does not already exist."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        id_role INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()


def _build_user_from_row(row):
    """Build a UserRole object from a database row."""
    if row is None:
        return None

    return UserRole(
        id_user=row[0],
        username=row[1],
        password=row[2],
        role=RoleBased(row[0], row[3])
    )


def check_permission(action, user_role):
    """Return True if the given role is allowed to perform the action."""
    if user_role is None:
        user_role = "visitor"

    permissions = {
        "visitor": {"get_all_horses", "get_horse"},
        "caregiver": {"add_horse", "update_horse", "get_horse"},
        "admin": {"add_horse", "update_horse", "update_distance", "delete_user", "get_horse", "delete_horse", "get_all_horses"},
    }

    return action in permissions.get(user_role, set())


def register_user(user):
    """Register a new user and save it to the database."""
    connection = connect()
    cursor = connection.cursor()

    id_role = user.role.id_role if user.role else 1  # default to visitor

    cursor.execute("""
    INSERT INTO users (username, password, id_role)
    VALUES (?, ?, ?)
    """, (user.username, user.password, id_role))

    connection.commit()
    connection.close()


def check_user_credentials(username, password):
    """Check credentials and return a UserRole object on success."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    connection.close()

    if row and row[2] == password:
        return _build_user_from_row(row)
    return None


def get_user_by_id(user_id):
    """Retrieve a user by its ID from the database."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE id_user = ?", (user_id,))
    row = cursor.fetchone()

    connection.close()
    return _build_user_from_row(row)


def get_user_by_role(role_id):
    """Retrieve all users that have the given role ID."""
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE id_role = ?", (role_id,))
    rows = cursor.fetchall()

    connection.close()
    return [_build_user_from_row(row) for row in rows]


def delete_user(user_id, user_role=None):
    """Delete a user by ID if the current role has permission."""
    if not check_permission("delete_user", user_role):
        raise PermissionError("Only admin can delete a user.")

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users WHERE id_user = ?", (user_id,))

    connection.commit()
    connection.close()