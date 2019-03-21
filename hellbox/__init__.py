from __future__ import print_function
import traceback
from .hellbox import Hellbox

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

__version__ = "0.0.2"
__all__ = ['Hellbox']


@Hellbox.proxy
def compose(*chutes):
    from .chute import CompositeChute

    def make_composite_chute():
        return CompositeChute(*chutes)

    return make_composite_chute


@Hellbox.proxy
def autoimport(path='requirements.txt'):
    from .autoimporter import Autoimporter
    Autoimporter(path).execute()


@Hellbox.proxy
def warn(*args, **kwargs):
    log('WARN', *args, **kwargs)


@Hellbox.proxy
def info(*args, **kwargs):
    log('INFO', *args, **kwargs)


@Hellbox.proxy
def log(level, message, trace=None):
    print("%s: %s" % (level, message))
    if trace:
        print("\n".join(traceback.format_tb(trace)))
