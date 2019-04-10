from setuptools import setup
from hellbox import __version__

setup(
    name="hellbox",
    version=__version__,
    author="Jack Jennings",
    author_email="jack@standard-library.com",
    packages=[
        "hellbox",
        "hellbox.chutes",
        "hellbox.jobs",
    ],
    url="http://github.com/hellboxpy/hellbox",
    license="LICENSE.txt",
    description="Build system for font development",
    long_description=open("README.rst").read(),
    install_requires=["glob2"],
)
