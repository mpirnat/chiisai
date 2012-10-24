from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()


version = '0.1'

install_requires = ['flask==0.9']

testing_extras = ['nose', 'mock']

setup(name='chiisai',
    version=version,
    description="a small URL shortener",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='url shortener',
    author='Mike Pirnat',
    author_email='mpirnat@gmail.com',
    url='http://github.com/mpirnat/chiisai',
    license='MIT',
    packages=['chiisai'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require = {
        'testing': testing_extras,
    },
    entry_points={}
)
