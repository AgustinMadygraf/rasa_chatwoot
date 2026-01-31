import subprocess
import sys
from urllib.parse import urlparse

from src.shared import config


def main() -> int:
    raw = (config.URL_WEBHOOK or "").strip()
    if not raw:
        print("ERROR: URL_WEBHOOK not set", file=sys.stderr)
        return 1
    # Accept full URL and extract host
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    domain = parsed.netloc or parsed.path
    domain = domain.split("/")[0].strip()
    if not domain:
        print("ERROR: URL_WEBHOOK must include a domain", file=sys.stderr)
        return 1

    cmd = ["ngrok", "http", "8000", "--domain", domain]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())

