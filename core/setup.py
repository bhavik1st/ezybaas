import os
from setuptools import find_packages, setup

from ezybaas import config 

def readme():
    with open('README.md') as f:
        return f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ezybaas',
    version= config.EZYBAAS_RELEASE_VERSION ,
    packages=find_packages(exclude=("ezybaasmain",)),
    install_requires=[
                    "Django>=2.2.1,<3.0.0",
                    "djangorestframework>=3.5.4",
                    "django-rest-swagger>=2.1.0",           
    ],
    include_package_data=True,
    license='Apache License',
    description="Easiest BaaS. Idea to APIs instantly on SQL DBs!",
    long_description=readme(),
    long_description_content_type="text/markdown",
    platforms=['any'],
    url='https://www.ezybaas.com/',
    author='Bhavik Shah',
    author_email='bhavik1st@gmail.com',
    keywords=['django', 'rest', 'database', 'api', 'baas', 'backend', 'backend as a service', 'rest'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        
    ],
)
