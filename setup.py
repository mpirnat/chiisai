from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()


version = '0.0'

install_requires = [
    'flask==0.9',
    'mock',
    'nose'
]


setup(name='chiisai',
    version=version,
    description="a small URL shortener",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='url shortener',
    author='Mike Pirnat',
    author_email='mpirnat@gmail.com',
    url='http://github.com/mpirnat/chiisai',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={}
)
