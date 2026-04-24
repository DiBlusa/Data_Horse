import sqlite3


def connect():
    return sqlite3.connect("horses.db")


def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        distance INTEGER NOT NULL DEFAULT 100,
        time INTEGER NOT NULL,
        theta_deg INTEGER NOT NULL DEFAULT 0
    )
    """)

    cursor.execute("PRAGMA table_info(horses)")
    columns = [column[1] for column in cursor.fetchall()]

    if "theta_deg" not in columns:
        cursor.execute("""
        ALTER TABLE horses
        ADD COLUMN theta_deg INTEGER NOT NULL DEFAULT 0
        """)

    connection.commit()
    connection.close()


def add_horse(horse):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO horses (name, distance, time, theta_deg)
    VALUES (?, ?, ?, ?)
    """, (horse.name, horse.distance, horse.time, horse.theta_deg))

    connection.commit()
    connection.close()


def update_horse(horse_id, new_name=None, new_time=None, new_theta_deg=None):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT name, time, theta_deg FROM horses
    WHERE id = ?
    """, (horse_id,))

    horse = cursor.fetchone()

    if horse is None:
        connection.close()
        return

    current_name, current_time, current_theta_deg = horse

    if new_name is None:
        new_name = current_name
    if new_time is None:
        new_time = current_time
    if new_theta_deg is None:
        new_theta_deg = current_theta_deg

    cursor.execute("""
    UPDATE horses
    SET name = ?, time = ?, theta_deg = ?
    WHERE id = ?
    """, (new_name, new_time, new_theta_deg, horse_id))

    connection.commit()
    connection.close()


def update_distance(horse_id, new_distance):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE horses
    SET distance = ?
    WHERE id = ?
    """, (new_distance, horse_id))

    connection.commit()
    connection.close()


def get_horse(horse_id):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM horses
    WHERE id = ?
    """, (horse_id,))

    horse = cursor.fetchone()
    connection.close()
    return horse


def get_all_horses():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM horses")
    horses = cursor.fetchall()

    connection.close()
    return horses
