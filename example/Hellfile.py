"""
    Example hellfile.py
    
    To run with development version of Hellbox, from this directory run:
    > hell init (This will fail because pip doesn't know about hellbox yet)
    > cd .. && ./example/.hellbox/bin/python setup.py install
    > cd example && hell freeze && hell inspect
"""

from hellbox import Hellbox
from hellbox.task import Task
from packages.test import TestUFO
from packages.generate_otf import GenerateOTF
from packages.extension import BuildRoboFontExtension

MakeOTF = Hellbox.compose(TestUFO(),
                          GenerateOTF(), 
                          Hellbox.write('otf'))

MakeExt = Hellbox.compose(BuildRoboFontExtension(info_format="yaml"),
                          Hellbox.write('.'))

with Hellbox('font') as task:
    task.describe('Does a little generation dance.')
    task.read('*.ufo', 'src/*') >> MakeOTF()

with Hellbox('extension') as task:
    task.describe('Builds a robofont extension in place.')
    task.requires('font')
    task.read('src') >> MakeExt()

Hellbox.default = 'font'
