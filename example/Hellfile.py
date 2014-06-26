"""
    Example hellfile.py
    
    To run with development version of Hellbox, from this directory run:
    > hell init (This will fail because pip doesn't know about hellbox yet)
    > cd .. && ./example/.hellbox/bin/python setup.py install
    > cd example && hell freeze && hell inspect
"""

from hellbox import Hellbox
from packages.test import TestUFO
from packages.generate_otf import GenerateOTF
from packages.extension import BuildRoboFontExtension

with Hellbox('font') as task:
    make_otf = Hellbox.compose(TestUFO(), GenerateOTF(), Hellbox.write('otf'))
    task.source('*.ufo', 'src/*').to(make_otf)

with Hellbox('extension') as task:
    build_extension = BuildRoboFontExtension(info_format="yaml")
    make_extension = Hellbox.compose(build_extension, Hellbox.write('.'))
    task.source('src').to(make_extension)

Hellbox.default = 'font'
