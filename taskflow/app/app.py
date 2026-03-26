from flask import Flask, render_template, request, redirect, url_for, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import sqlite3
import os

app = Flask(__name__)

# ─── Prometheus Metrics ───────────────────────────────────────────
REQUEST_COUNT = Counter(
    'flask_http_request_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

@app.after_request
def track_requests(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    return response

# ─── Database setup ───────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# ─── Routes ───────────────────────────────────────────────────────
@app.route("/")
def home():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("home.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form["task"]
    conn = get_db()
    conn.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/done/<int:id>")
def mark_done(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    explanation = ""
    if request.method == "POST":
        log_text = request.form["log"]
        from ai_assistant import analyze_log
        explanation = analyze_log(log_text)
    return render_template("analyze.html", explanation=explanation)

# ─── Run ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)