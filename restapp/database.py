from .app import app, get_db


def init_db():
    """
    Initialize our database by create a couple tables
    """
    with app.app_context():
        db = get_db().cursor()
        res = db.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users'
            """)

        if not res.fetchall():
            db.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT,
                    favorite_color TEXT
                )""")
