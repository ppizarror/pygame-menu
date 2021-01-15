del dist\*.* /s /q
del build\*.* /s /q
py -3.7-64 setup.py sdist bdist_wheel