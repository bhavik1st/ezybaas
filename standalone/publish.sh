#!/bin/bash
set echo off

cd ..
cd core

if [ $1 = "prod" ]
    then
        echo "*** Publishing django-ezybaas to PyPI ***"
        python3 -m twine upload  dist/*
    else
        echo "*** Publishing django-ezybaas to Test PyPI ***"
        python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
fi
#rem python3 -m pip install --user --upgrade setuptools wheel
#rem python3 setup.py sdist bdist_wheel
#rem python3 -m pip install --user --upgrade twine
#rem python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#rem https://packaging.python.org/tutorials/packaging-projects/
# python3 -m twine upload  dist/*

#rm -rf dist/
#python3 setup.py sdist bdist_wheel
#cp dist/django-ezybaas-*.tar.gz ../standalone/ 
echo "*** Published django-ezybaas ***"
set echo on
