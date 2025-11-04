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

# Cache the rendered HTML to avoid re-executing on every request
_cached_html = None


def render_notebook(timeout=1200, use_cache=True):
    """Execute the notebook and return HTML. Increased timeout for complex notebooks."""
    global _cached_html
    
    # Return cached version if available and caching is enabled
    if use_cache and _cached_html is not None:
        return _cached_html
    
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
    # Allow errors to show which cell failed
    client = NotebookClient(
        nb, 
        timeout=timeout, 
        kernel_name="python3",
        allow_errors=True,  # Continue execution even if a cell fails
        store_widget_state=True  # Preserve interactive widgets
    )
    client.execute()

    # Configure HTMLExporter to properly embed interactive plots
    exporter = HTMLExporter()
    # Use the 'lab' template which includes better support for interactive outputs
    # and ensures Plotly/widget resources are included
    exporter.template_name = 'lab'
    
    # Alternative: you can also configure to embed resources
    # exporter.exclude_input = False  # Keep code cells visible
    
    body, resources = exporter.from_notebook_node(nb)
    
    # Cache the result
    _cached_html = body
    
    return body


@app.route("/")
def index():
    try:
        html = render_notebook(use_cache=True)
        return Response(html, mimetype="text/html")
    except Exception as e:
        tb = traceback.format_exc()
        error_msg = f"""
        <html>
        <head><title>Error Loading Notebook</title></head>
        <body>
            <h1>⚠️ Error Rendering Notebook</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <h2>Troubleshooting:</h2>
            <ul>
                <li>First load takes 10-15 minutes (notebook execution)</li>
                <li>Try refreshing the page in a few minutes</li>
                <li>Visit <a href="/refresh">/refresh</a> to force reload</li>
            </ul>
            <h2>Full Error Details:</h2>
            <pre style="background:#f4f4f4;padding:15px;overflow:auto;">{tb}</pre>
        </body>
        </html>
        """
        return Response(error_msg, mimetype="text/html"), 500


@app.route("/refresh")
def refresh():
    """Force re-render of the notebook (clears cache)."""
    global _cached_html
    _cached_html = None
    try:
        html = render_notebook(use_cache=False)
        return Response(html, mimetype="text/html")
    except Exception as e:
        tb = traceback.format_exc()
        error_msg = f"""
        <html>
        <head><title>Error Loading Notebook</title></head>
        <body>
            <h1>⚠️ Error Rendering Notebook</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <h2>Full Error Details:</h2>
            <pre style="background:#f4f4f4;padding:15px;overflow:auto;">{tb}</pre>
        </body>
        </html>
        """
        return Response(error_msg, mimetype="text/html"), 500


@app.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "cached": _cached_html is not None}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
