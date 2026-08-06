import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "workshopuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "workshop123")
DB_NAME = os.environ.get("DB_NAME", "notesdb")


def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )


def init_db():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, title, content FROM notes ORDER BY id DESC")
            notes = cur.fetchall()
        return jsonify(notes)
    finally:
        conn.close()


@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "title and content are required"}), 400
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, title, content",
                (data["title"], data["content"]),
            )
            note = cur.fetchone()
        conn.commit()
        return jsonify(note), 201
    finally:
        conn.close()


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
