#!/bin/bash
set echo off
echo "*** Building django-ezybaas ***"
#rem python3 -m pip install --user --upgrade setuptools wheel
#rem python3 setup.py sdist bdist_wheel
#rem python3 -m pip install --user --upgrade twine
#rem python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#rem https://packaging.python.org/tutorials/packaging-projects/
# python3 -m twine upload  dist/*
rm django-ezybaas-*.tar.gz
cd ..
cd core
rm -rf dist/
python3 setup.py sdist bdist_wheel
cp dist/django-ezybaas-*.tar.gz ../standalone/ 
echo "*** Built django-ezybaas ***"
set echo on
