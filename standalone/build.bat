@echo off
echo "*** Building django-ezybaas ***"
rem python -m pip install --user --upgrade setuptools wheel
rem python setup.py sdist bdist_wheel
rem 
cd ..
cd core
del /F /S /Q dist/
python setup.py sdist
copy dist\django-ezybaas-*.tar.gz ..\standalone\ 
@echo on
echo "*** Built django-ezybaas ***"