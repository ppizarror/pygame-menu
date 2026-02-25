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

assert len(sys.argv) == 2, 'Argument is required, usage: build.py pip/twine'
mode: str = sys.argv[1].strip()

root = Path(__file__).resolve().parent
dist = root / 'dist'
build = root / 'build'

if mode == 'pip':
    if dist.is_dir():
        for k in dist.iterdir():
            if 'pygame_menu-' in k.name or 'pygame-menu-' in k.name:
                k.unlink()

    if build.is_dir():
        for k in build.iterdir():
            if 'bdist.' in k.name or k.name == 'lib':
                shutil.rmtree(k)

    subprocess.run(
        ["python", "setup.py", "sdist", "bdist_wheel"],
        check=True
    )

elif mode == 'twine':
    if dist.is_dir():
        subprocess.run(
            ["python", "-m", "twine", "upload", "dist/*"],
            shell=True,   # required because of wildcard
            check=True
        )
    else:
        raise FileNotFoundError('No distribution found, execute build.py pip first')

else:
    raise ValueError(f'Unknown mode {mode}')
