from setuptools import setup, find_packages
import sys, os
from glob import glob


version = '0.10'

setup(name='netflowindexer_web',
    version=version,
    description="Simple web interface for netflow-indexer",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='netflowindexer web',
    author='Justin Azoff',
    author_email='JAzoff@uamail.albany.edu',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    py_modules=['netflowindexer_web'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "bottle",
        "netflowindexer>=0.1.21",
    ],
    scripts=glob('scripts/*'),
    entry_points = {
        'console_scripts': [
            'netflow-indexer-web = netflowindexer_web:main',
        ]
    },
    )
