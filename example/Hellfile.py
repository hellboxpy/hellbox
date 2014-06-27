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

make_otf = Hellbox.compose(TestUFO(), GenerateOTF(), Hellbox.write('otf'))
build_extension = BuildRoboFontExtension(info_format="yaml")
make_extension = Hellbox.compose(build_extension, Hellbox.write('.'))

with Hellbox('font') as task:
    task.source('*.ufo', 'src/*').to(make_otf)

with Hellbox('extension') as task:
    task.source('src').to(make_extension)

task = Task('foobar')
task.source('*.ufo').to(make_otf)
Hellbox.add_task(task)

Hellbox.default = 'font'
