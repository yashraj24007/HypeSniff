from pathlib import Path
import traceback
import os
import sys
import json

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

    # Ensure a usable kernelspec is available so nbclient can start a kernel
    # (On Render there may be no system kernelspecs installed.) We create a
    # small kernelspec that points to the current Python interpreter and
    # expose it via JUPYTER_PATH so jupyter_client can discover it.
    jupyter_data_dir = ROOT / "jupyter_data"
    kernelspec_dir = jupyter_data_dir / "kernels" / "python3"
    if not kernelspec_dir.exists():
        kernelspec_dir.mkdir(parents=True, exist_ok=True)
        kernel_json = {
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Python 3",
            "language": "python",
        }
        (kernelspec_dir / "kernel.json").write_text(json.dumps(kernel_json))

    # Add our generated jupyter_data_dir to JUPYTER_PATH so KernelSpecManager
    # will see the kernelspec above.
    os.environ.setdefault("JUPYTER_PATH", str(jupyter_data_dir))

    nb = nbformat.read(str(NOTEBOOK_PATH), as_version=4)

    # Create the NotebookClient and execute. Explicitly request the 'python3'
    # kernel name so it uses the kernelspec we just created.
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3")
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
