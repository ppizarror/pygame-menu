"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYPROJECT UPDATE
Updates pyproject toml with library metadata.

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

import pygame_menu

with open('pyproject.toml') as f:
    pyproject = []
    for line in f:
        pyproject.append(line.strip())

# Configure tool.poetry
i0 = pyproject.index('[tool.poetry]')
for i in range(i0, len(pyproject)):
    if 'name = ' in pyproject[i]:
        pyproject[i] = 'name = "{}"'.format(pygame_menu.__module_name__)
    elif 'version = ' in pyproject[i]:
        pyproject[i] = 'version = "{}"'.format(pygame_menu.__version__)
    elif 'description = ' in pyproject[i]:
        pyproject[i] = 'description = "{}"'.format(pygame_menu.__description__)
    elif pyproject[i] == 'authors = ':
        pyproject[i] = 'authors = ["{}"]'.format(pygame_menu.__author__)
    elif pyproject[i] == '':
        break

with open('pyproject.toml', 'w') as f:
    for line in pyproject:
        f.write(line + '\n')
