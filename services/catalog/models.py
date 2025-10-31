import sqlite3, json, os

DB = os.getenv("CATALOG_DB_PATH", "catalog.db")


def init():
    with sqlite3.connect(DB) as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS books(
            id TEXT PRIMARY KEY, title TEXT, author TEXT, genres TEXT, rating REAL)"""
        )


def add_book(b):
    with sqlite3.connect(DB) as c:
        c.execute(
            "INSERT OR REPLACE INTO books(id,title,author,genres,rating) VALUES(?,?,?,?,?)",
            (b["id"], b["title"], b["author"], json.dumps(b["genres"]), b["rating"]),
        )
        c.commit()


def get_book(id_):
    with sqlite3.connect(DB) as c:
        cur = c.execute(
            "SELECT id,title,author,genres,rating FROM books WHERE id=?", (id_,)
        )
        row = cur.fetchone()
        return (
            None
            if not row
            else {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "genres": json.loads(row[3] or "[]"),
                "rating": row[4],
            }
        )


def list_books():
    with sqlite3.connect(DB) as c:
        cur = c.execute("SELECT id,title,author,genres,rating FROM books")
        return [
            {
                "id": r[0],
                "title": r[1],
                "author": r[2],
                "genres": json.loads(r[3] or "[]"),
                "rating": r[4],
            }
            for r in cur.fetchall()
        ]


def search(q):
    q = f"%{q.lower()}%"
    with sqlite3.connect(DB) as c:
        cur = c.execute(
            """SELECT id,title,author,genres,rating FROM books
                           WHERE lower(title) LIKE ? OR lower(author) LIKE ?""",
            (q, q),
        )
        return [
            {
                "id": r[0],
                "title": r[1],
                "author": r[2],
                "genres": json.loads(r[3] or "[]"),
                "rating": r[4],
            }
            for r in cur.fetchall()
        ]


def clear():
    with sqlite3.connect(DB) as c:
        cur = c.execute("SELECT COUNT(1) FROM books")
        (n,) = cur.fetchone()
        c.execute("DELETE FROM books")
        c.commit()
        return n