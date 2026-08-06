import os

import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8080")


@app.route("/")
def index():
    error = None
    notes = []
    try:
        resp = requests.get(f"{BACKEND_URL}/api/notes", timeout=5)
        resp.raise_for_status()
        notes = resp.json()
    except Exception as e:
        error = f"Could not reach backend: {e}"
    return render_template("index.html", notes=notes, error=error)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Title and content are required.")
        return redirect(url_for("index"))
    try:
        resp = requests.post(
            f"{BACKEND_URL}/api/notes",
            json={"title": title, "content": content},
            timeout=5,
        )
        resp.raise_for_status()
    except Exception as e:
        flash(f"Failed to save note: {e}")
    return redirect(url_for("index"))


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
