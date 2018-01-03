import codecs
from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup

import neojsonrpc


def read_relative_file(filename):
    """ Returns contents of the given file, whose path is supposed relative to this module. """
    with codecs.open(join(dirname(abspath(__file__)), filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='neojsonrpc',
    version=neojsonrpc.__version__,
    author='Morgan Aubert',
    author_email='morgan.aubert@zoho.com',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    url='https://github.com/ellmetha/neojsonrpc',
    license='MIT',
    description='A Python JSON-RPC client for the NEO blockchain.',
    long_description=read_relative_file('README.rst'),
    keywords='neo blockchain json-rpc json-rpc-client api',
    zip_safe=False,
    install_requires=[
        'requests>2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
