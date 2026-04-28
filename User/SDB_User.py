import sqlite3

def connect():
    return sqlite3.connect("SDB_User.db")

def create_table():
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

def check_permission(action, user_role):
    if user_role is None:
        user_role = "visitor"

    permissions = {
        "visitor": {"get_all_horses", "get_horse"},
        "caregiver": {"add_horse", "update_horse", "get_horse"},
        "admin": {"add_horse", "update_horse", "update_distance", "get_horse", "delete_horse", "get_all_horses"},
    }

    return action in permissions.get(user_role, set())

def register_user(user):
    connection = connect()
    cursor = connection.cursor()

    id_role = user.role.id_role if user.role else 1  # 1 é visitor por padrão

    cursor.execute("""
    INSERT INTO users (username, password, id_role)
    VALUES (?, ?, ?)
    """, (user.username, user.password, id_role))

    connection.commit()
    connection.close()

def check_user_credentials(username, password):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    connection.close()

    if row and row[2] == password:
        return UserRole(id_user=row[0], username=row[1], role=RoleBased(row[0], row[3]))
    return None

def get_user_by_id(user_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE id_user = ?", (user_id,))
    row = cursor.fetchone()

    connection.close()

    if row:
        return UserRole(id_user=row[0], username=row[1], role=RoleBased(row[0], row[3]))
    return None

def get_user_by_role(role_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT id_user, username, password, id_role FROM users WHERE id_role = ?", (role_id,))
    rows = cursor.fetchall()

    connection.close()

    return [UserRole(id_user=row[0], username=row[1], role=RoleBased(row[0], row[3])) for row in rows]

def delete_user(user_id):
    if not check_permission("delete_user", user_role):
        raise PermissionError("Apenas o admin pode deletar um usuário.")
   
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users WHERE id_user = ?", (user_id,))

    connection.commit()
    connection.close()