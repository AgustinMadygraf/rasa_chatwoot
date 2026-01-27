import os
import subprocess
import sys
from urllib.parse import urlparse

from src.shared import config


def _extract_port(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    if parsed.port:
        return str(parsed.port)
    return "5005"


def main() -> int:
    url = (config.RASA_REST_URL or "").strip()
    if not url:
        print("ERROR: RASA_REST_URL not set", file=sys.stderr)
        return 1
    rasa_project = os.path.join("src", "infrastructure", "rasa")
    port = _extract_port(url)
    cmd = [sys.executable, "-m", "rasa", "run", "--enable-api", "--cors", "*", "--port", port]
    return subprocess.call(cmd, cwd=rasa_project)


if __name__ == "__main__":
    raise SystemExit(main())
