"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUILD

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import os
import sys

assert len(sys.argv) == 2, 'Argument is required, usage: build.py pip/twine/gource'
mode = sys.argv[1].strip()
python = 'python3' if not sys.platform == 'win32' else 'py -3.7'

if mode == 'pip':
    if os.path.isdir('dist/pip'):
        for k in os.listdir('dist/pip'):
            if 'pygame_menu-' in k:
                os.remove(f'dist/pip/{k}')
    if os.path.isdir('build'):
        for k in os.listdir('build'):
            if 'bdist.' in k or k == 'lib':
                os.system(f'rm -rf build/{k}')
    os.system(f'{python} setup.py sdist --dist-dir dist/pip bdist_wheel --dist-dir dist/pip')

elif mode == 'twine':
    if os.path.isdir('dist/pip'):
        os.system(f'{python} -m twine upload dist/pip/*')
    else:
        raise FileNotFoundError('Not distribution been found, execute build.py pip first')

elif mode == 'gource':
    os.system('gource -s 0.25 --title pygame-menu --disable-auto-rotate --key '
              '--highlight-users --disable-bloom --multi-sampling -w --transparent --path ./')

else:
    raise ValueError(f'Unknown mode {mode}')
