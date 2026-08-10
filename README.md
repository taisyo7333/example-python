# example-python

## Flask + PostgreSQL

A Flask app that reads task data from PostgreSQL and displays it as an HTML table.
In OpenShift Dev Spaces, PostgreSQL runs as a **sidecar container** in the same workspace pod (defined in `devfile.yaml`).

### Prerequisites (Dev Spaces)

1. Restart the workspace after changing `devfile.yaml` so the `postgres` container starts.
2. Run the commands below in order.

### Setup

Installs **Python 3.14** via [uv](https://docs.astral.sh/uv/) (UDI default is older), creates `.venv`, and installs dependencies:

```bash
./scripts/setup-flask.sh
```

Or use Dev Spaces command **01-setup-flask-app**.

To pin another version: `PYTHON_VERSION=3.13 ./scripts/setup-flask.sh`.

### Load CSV data

```bash
./scripts/load-csv.sh
```

Or use Dev Spaces command **02-load-csv-data**.

This creates the `tasks` table and loads rows from `data/tasks.csv`.

### Run

```bash
./scripts/run-flask.sh
```

Or use Dev Spaces command **03-run-flask-app**.

Open the Flask endpoint in your browser to see the task list from the database.

### Connection

Default connection string (also set in `devfile.yaml`):

```text
DATABASE_URL=postgresql://app:app@localhost:5432/appdb
```

`localhost` works because the Flask and PostgreSQL containers share the workspace pod network.

Outside Dev Spaces, point `DATABASE_URL` at your local PostgreSQL instance.

### Container image (podman)

Flask イメージも開発環境と同じ **Python 3.14**（`ubi9/python-314`）を使います。

Build, run, and push the Flask image to the OpenShift internal registry.

```bash
./scripts/podman-build.sh
./scripts/podman-run.sh
./scripts/podman-push.sh
```

Or use Dev Spaces commands **04-podman-build**, **05-podman-run**, **06-podman-push**.

Default image:

```text
image-registry.openshift-image-registry.svc:5000/<namespace>/example-python-flask:latest
```

Override with `IMAGE_TAG`, `NAMESPACE`, `FULL_IMAGE`, or `DATABASE_URL` as needed.

`podman run` starts Flask only. Without a reachable Postgres, `/` returns HTTP 503. Pass a reachable URL, for example:

```bash
DATABASE_URL=postgresql://app:app@host.containers.internal:5432/appdb ./scripts/podman-run.sh
```

