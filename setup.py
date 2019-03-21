from setuptools import setup
from hellbox import __version__

setup(
    name='hellbox',
    version=__version__,
    author='Jack Jennings',
    author_email='j@ckjennin.gs',
    packages=['hellbox'],
    url='http://github.com/jackjennings/hellbox',
    license='LICENSE.txt',
    description='Build system for font development',
    long_description=open('README.rst').read(),
    install_requires=[
        'virtualenv',
        'glob2'
    ]
)
