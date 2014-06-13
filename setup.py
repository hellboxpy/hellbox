from setuptools import setup
import hellbox

setup(
    name='hellbox',
    version=hellbox.__version__,
    author='Jack Jennings',
    author_email='j@ckjennin.gs',
    packages=['hellbox', 'hellbox.test'],
    url='http://github.com/jackjennings/hellbox',
    license='LICENSE.txt',
    description='Build system for font development',
    long_description=open('README.rst').read(),
    install_requires=hellbox.__self_requirements__,
    entry_points={
        "console_scripts": [
            "hell=hellbox:main"
        ]
    }
)
