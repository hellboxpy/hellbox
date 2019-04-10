import traceback
from .hellbox import Hellbox
from .chute import Chute

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

__all__ = [
    "Chute",
    "Hellbox"
]


@Hellbox.proxy
def compose(*chutes):
    from .chutes.composite import CompositeChute

    def make_composite_chute():
        return CompositeChute(*chutes)

    return make_composite_chute


@Hellbox.proxy
def autoimport(path="Pipfile.lock"):
    from .autoimporter import Autoimporter

    Autoimporter(path).execute(globals(), locals())


@Hellbox.proxy
def debug(*args, **kwargs):
    log("⋯", *args, **kwargs)


@Hellbox.proxy
def info(*args, **kwargs):
    log("ℹ", *args, **kwargs)


@Hellbox.proxy
def warn(*args, **kwargs):
    log("⚠", *args, **kwargs)


@Hellbox.proxy
def error(*args, **kwargs):
    log("�", *args, **kwargs)


@Hellbox.proxy
def log(level, message, trace=None):
    print("%s \u2502 %s" % (level, message))
    if trace:
        print("\n".join(traceback.format_tb(trace)))
