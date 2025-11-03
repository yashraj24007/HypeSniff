from pathlib import Path
import traceback

from flask import Flask, Response

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

# Minimal app: executes and serves the whole notebook as HTML
ROOT = Path(__file__).parent
NOTEBOOK_PATH = ROOT / "DAV_project_1_v2.ipynb"

app = Flask(__name__)


def render_notebook(timeout=600):
    """Execute the notebook and return HTML. This is intentionally minimal."""
    if not NOTEBOOK_PATH.exists():
        raise FileNotFoundError(f"Notebook not found at {NOTEBOOK_PATH}")

    nb = nbformat.read(str(NOTEBOOK_PATH), as_version=4)

    client = NotebookClient(nb, timeout=timeout)
    client.execute()

    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(nb)
    return body


@app.route("/")
def index():
    try:
        html = render_notebook()
        return Response(html, mimetype="text/html")
    except Exception:
        tb = traceback.format_exc()
        return Response(f"<h1>Error rendering notebook</h1><pre>{tb}</pre>", mimetype="text/html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
