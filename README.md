# example-python

[![Contribute](https://www.eclipse.org/che/contribute.svg)](https://devspaces.apps.rosa.ihjzx-45uit-hus.jbid.p3.openshiftapps.com#https://github.com/taisyo7333/example-python/tree/git-provider-github)

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