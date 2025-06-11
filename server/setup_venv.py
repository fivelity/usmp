import os
import subprocess
import sys


def create_venv():
    venv_dir = "venv"
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    subprocess.check_call(
        [os.path.join(venv_dir, "bin", "pip"), "install", "-r", "requirements-dev.txt"]
    )


if __name__ == "__main__":
    create_venv()
