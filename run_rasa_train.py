import os
import subprocess
import sys


def main() -> int:
    rasa_project = os.path.join("src", "infrastructure", "rasa")
    cmd = [sys.executable, "-m", "rasa", "train"]
    return subprocess.call(cmd, cwd=rasa_project)


if __name__ == "__main__":
    raise SystemExit(main())
