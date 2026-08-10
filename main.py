import html
import os

import psycopg
from flask import Flask, Response


app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://app:app@localhost:5432/appdb"
)


def fetch_tasks() -> list[tuple[int, str, bool]]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
            return list(cur.fetchall())


@app.get("/")
def index() -> Response | str:
    try:
        tasks = fetch_tasks()
    except Exception as exc:  # noqa: BLE001 - surface DB errors to the browser
        return Response(
            f"<h1>Database error</h1><pre>{html.escape(str(exc))}</pre>"
            "<p>Run <code>02-load-csv-data</code> after PostgreSQL is ready.</p>",
            status=503,
            mimetype="text/html",
        )

    rows = "".join(
        "<tr>"
        f"<td>{task_id}</td>"
        f"<td>{html.escape(title)}</td>"
        f"<td>{'done' if done else 'todo'}</td>"
        "</tr>"
        for task_id, title, done in tasks
    )
    return (
        "<!DOCTYPE html>"
        "<html><head><meta charset='utf-8'><title>Tasks</title>"
        "<style>"
        "body{font-family:system-ui,sans-serif;margin:2rem;}"
        "table{border-collapse:collapse;}"
        "th,td{border:1px solid #ccc;padding:0.5rem 0.75rem;text-align:left;}"
        "th{background:#f5f5f5;}"
        "</style></head><body>"
        "<h1>Tasks</h1>"
        "<table><thead><tr><th>ID</th><th>Title</th><th>Status</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "</body></html>"
    )


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=debug, host="0.0.0.0", port=port)
