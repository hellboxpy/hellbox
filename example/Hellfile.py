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

with Hellbox('font') as task:
    task.describe('Does a little generation dance.')

    make_otf = Hellbox.compose(TestUFO(), GenerateOTF(), Hellbox.write('otf'))
    # make_otf = Hellbox.write('otf') << GenerateOTF() << TestUFO()

    task.source('*.ufo', 'src/*') >> make_otf

with Hellbox('extension') as task:
    task.describe('Builds a robofont extension in place.')

    build_extension = BuildRoboFontExtension(info_format="yaml")
    make_extension = Hellbox.compose(build_extension, Hellbox.write('.'))

    task.source('src') >> make_extension

task = Task('foobar')
task.source('*.ufo').to(make_otf)
Hellbox.add_task(task)

Hellbox.default = 'font'
