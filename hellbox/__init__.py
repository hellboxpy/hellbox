from __future__ import print_function
import os
import sys
import subprocess
import traceback
from argparse import ArgumentParser
from .hellbox import Hellbox

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

__version__ = "0.0.2"
__all__ = ['Hellbox']


@Hellbox.proxy
def compose(*chutes):
    from .chute import CompositeChute
    def composite():
        return CompositeChute(*chutes)
    return composite

@Hellbox.proxy
def write(path):
    from .chute import WriteFiles
    return WriteFiles(path)


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


def main():

    executable_filename = 'Hellfile.py'
    requirements_filename = 'requirements.txt'
    virtualenv_dir = '.hellbox'
    bin_dir = './%s/bin' % virtualenv_dir
    path_to_pip = '%s/pip' % bin_dir
    path_to_python = '%s/python' % bin_dir
    path_to_hell = '%s/hell' % bin_dir
    path_to_requirements = './%s' % requirements_filename

    def init(options=None):
        path = os.getcwd()
        create_virtualenv(path)
        if os.path.exists(path_to_requirements):
            install_requirements()
        else:
            install_package('git+git://github.com/jackjennings/hellbox.git')
        freeze_requirements()
        create_hellbox_py(path)

    def create_virtualenv(path):
        if not os.path.isdir(virtualenv_dir):
            subprocess.call(['virtualenv', os.path.join(path, virtualenv_dir)])

    def create_hellbox_py(path):
        path = os.path.join(path, executable_filename)
        content = "from hellbox import Hellbox\n\nHellbox.autoimport()"
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)

    def freeze(options):
        freeze_requirements()

    def freeze_requirements():
        cmd = [path_to_pip, 'freeze', '--local']
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        requirements, err = output.communicate()
        with open(path_to_requirements, 'w') as f:
            f.write(requirements)

    def install(options=None):
        if options and options.package:
            install_package(options.package)
        else:
            install_requirements()
        freeze_requirements()

    def install_requirements():
        cmd = [path_to_pip, 'install', '-r', path_to_requirements]
        subprocess.call(cmd)

    def install_package(package):
        cmd = [path_to_pip, 'install', package]
        subprocess.call(cmd)

    def uninstall(options):
        cmd = [path_to_pip, 'uninstall', options.package, '--yes']
        subprocess.call(cmd)
        freeze_requirements()

    def run(options):
        if not os.path.exists(executable_filename):
            print('No %s found' % executable_filename)
            return

        if not os.path.isdir(virtualenv_dir):
            init()

        run_task(options.task or "default")

    def run_hellfile_commands(commands=None):
        script = [
            'execfile("%s")' % executable_filename,
            'import hellbox'
        ]
        if commands is not None:
            script.extend(commands)
        cmd = [path_to_python, '-c', ';'.join(script)]
        subprocess.call(cmd)

    def run_task(task):
        run_hellfile_commands(['hellbox.Hellbox.run_task("%s")' % task])

    def inspect(options):
        run_hellfile_commands(['hellbox.Hellbox.inspect()'])

    parser = ArgumentParser(description="""
        Lightweight wrapper around virtualenv and pip for running the Hellbox
        toolchain
    """)
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init', description="""
        Creates a isolated environment in .hellbox for installing
        plugins and dependencies and creates a blank Hellfile to define
        tasks within.
    """)
    init_parser.set_defaults(func=init)

    freeze_parser = subparsers.add_parser('freeze', description="""
        Records dependencies into requirements.txt
    """)
    freeze_parser.set_defaults(func=freeze)

    install_parser = subparsers.add_parser('install', description="""
        Installs a package and freezes dependencies, or installs all
        dependencies from requirements.txt if no package specified
    """)
    install_parser.add_argument('package', nargs='?')
    install_parser.set_defaults(func=install)

    uninstall_parser = subparsers.add_parser('uninstall', description="""
        Uninstalls a package and freezes dependencies
    """)
    uninstall_parser.add_argument('package')
    uninstall_parser.set_defaults(func=uninstall)

    run_parser = subparsers.add_parser('run', description="""
        Runs a task defined in %s
    """ % executable_filename)
    run_parser.add_argument('task', nargs='?')
    run_parser.set_defaults(func=run)

    inspect_parser = subparsers.add_parser('inspect', description="""""")
    inspect_parser.set_defaults(func=inspect)

    namespace = parser.parse_args()
    namespace.func(namespace)
