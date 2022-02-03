"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUILD
Build file.
"""

import os
import sys

assert len(sys.argv) == 2, 'Argument is required, usage: build.py pip/twine/gource'
mode = sys.argv[1].strip()
python = 'python3' if not sys.platform == 'win32' else 'py -3.8'

if mode == 'pip':
    if os.path.isdir('dist'):
        for k in os.listdir('dist'):
            if 'pygame_menu-' in k or 'pygame-menu-' in k:
                os.remove(f'dist/{k}')
    if os.path.isdir('build'):
        for k in os.listdir('build'):
            if 'bdist.' in k or k == 'lib':
                os.system(f'rm -rf build/{k}')
    os.system(f'{python} setup.py sdist bdist_wheel')

elif mode == 'twine':
    if os.path.isdir('dist'):
        os.system(f'{python} -m twine upload dist/*')
    else:
        raise FileNotFoundError('Not distribution been found, execute build.py pip')

elif mode == 'gource':
    os.system('gource -s 0.25 --title pygame-menu --disable-auto-rotate --key '
              '--highlight-users --disable-bloom --multi-sampling -w --transparent --path ./')

else:
    raise ValueError(f'Unknown mode {mode}')
