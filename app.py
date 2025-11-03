from pathlib import Path
from flask import Flask, send_file, Response

# Serve pre-rendered notebook HTML
ROOT = Path(__file__).parent
HTML_PATH = ROOT / "notebook_output.html"

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the pre-rendered notebook HTML."""
    if HTML_PATH.exists():
        return send_file(HTML_PATH, mimetype="text/html")
    else:
        return Response(
            "<h1>Error</h1><p>Pre-rendered notebook not found. "
            "Please ensure the build process completed successfully.</p>",
            mimetype="text/html"
        ), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
