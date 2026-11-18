"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUILD
Build file.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

assert len(sys.argv) == 2, "Argument is required, usage: build_package.py pip/twine"

mode = sys.argv[1].strip()

root = Path(__file__).resolve().parent
dist = root / "dist"
build = root / "build"


if mode == "pip":
    if dist.is_dir():
        shutil.rmtree(dist)

    if build.is_dir():
        shutil.rmtree(build)

    subprocess.run(
        [sys.executable, "-m", "build"],
        check=True,
    )

elif mode == "twine":
    if not dist.is_dir():
        raise FileNotFoundError(
            "No distribution found, execute build_package.py pip first"
        )

    distributions = sorted(str(path) for path in dist.iterdir() if path.is_file())

    if not distributions:
        raise FileNotFoundError("No distribution artifacts found in dist/")

    subprocess.run(
        [sys.executable, "-m", "twine", "upload", *distributions],
        check=True,
    )

else:
    raise ValueError(f"Unknown mode {mode}")
