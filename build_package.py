"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUILD
Build file.
"""

import shutil
import subprocess
import sys
from pathlib import Path

assert len(sys.argv) == 2, "Argument is required, usage: build_package.py pip/twine"
mode: str = sys.argv[1].strip()

root = Path(__file__).resolve().parent
dist = root / "dist"
build = root / "build"

if mode == "pip":
    if dist.is_dir():
        shutil.rmtree(dist)

    if build.is_dir():
        shutil.rmtree(build)

    subprocess.run(["python", "-m", "build"], check=True)

elif mode == "twine":
    if dist.is_dir():
        subprocess.run(
            ["python", "-m", "twine", "upload", "dist/*"],
            shell=True,  # required because of wildcard
            check=True,
        )
    else:
        raise FileNotFoundError(
            "No distribution found, execute build_package.py pip first"
        )

else:
    raise ValueError(f"Unknown mode {mode}")
