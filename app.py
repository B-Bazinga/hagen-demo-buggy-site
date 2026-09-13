"""QuickNotes -- a small notes app used as the intentionally-buggy demo site
for Hagen's self-healing incident-response walkthrough.

The bug lives in admin_restart(): the auth check below is supposed to allow
a restart only when the caller supplies the exact ADMIN_TOKEN, but the
`or token == ""` clause means an *empty* token is treated as valid too --
so anyone who hits /admin/restart with no token at all can force the
process to exit. That's the "crash" for this demo. The real fix is a
one-line change: drop the `or token == ""` clause.
"""
import os
import time

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "change-me-in-prod")
START_TIME = time.time()

NOTES = [
    {"title": "Welcome to QuickNotes", "body": "This is a demo notes app. Add your own note below."},
    {"title": "Roadmap", "body": "Tags, search, and dark mode are coming soon."},
]


@app.route("/")
def index():
    return render_template("index.html", notes=NOTES)


@app.route("/notes", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    if title and body:
        NOTES.insert(0, {"title": title, "body": body})
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return jsonify(status="ok", service="quicknotes", uptime_seconds=round(time.time() - START_TIME, 1))


@app.route("/admin/restart")
def admin_restart():
    token = request.args.get("token", "")
    # BUG: an empty token should never be treated as authorized.
    if token == ADMIN_TOKEN or token == "":
        os._exit(1)
    return jsonify(error="forbidden"), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
