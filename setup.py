from setuptools import setup

setup(
    name='Hellbox',
    version='0.1.0',
    author='Jack Jennings',
    author_email='j@ckjennin.gs',
    packages=['hellbox', 'hellbox.test'],
    url='http://github.com/jackjennings/Hellbox',
    license='LICENSE.txt',
    description='Build system for font development',
    long_description=open('README.rst').read(),
    install_requires=[
        'virtualenv'
    ],
    entry_points={
        "console_scripts": [
            "hell=hellbox:main"
        ]
    }
)
