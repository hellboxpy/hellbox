Hellbox
=======

Hellbox is a modular, editor-agnostic build system designed for font development.

**Hellbox is in the early stages of development. This document is more of a roadmap than documentation of the current implementation. Expect API changes without notice until v0.1.**

.. image:: https://travis-ci.org/hellboxpy/hellbox.svg?branch=master
    :target: https://travis-ci.org/hellboxpy/hellbox

.. code-block:: python
  
    from hellbox import Hellbox
    from hellbox_generate_otf import GenerateOTF

    with Hellbox('build') as task:
        task.describe('Builds .otf files from .ufo source')
        task.read('*.ufo') >> GenerateOTF() >> task.write('./otf')

Installation
------------

First `install pip`_ (if not present), then run:

``pip install git+git://github.com/jackjennings/hellbox.git``

Goals
-----

* **Consistency** Hellbox tasks don't take arguments by design, favoring consistent task output
* **Modularity** Hellbox packages should be resuable and composable, while maintaining flexibility for custom workflows
* **Isolation** Hellbox tasks and packages are version locked and isolated from other Python installations

Chutes
------

There are two ways of defining a Hellbox chute, depending on the complexity and amount of configuration required.

The basic setup for defining your own chutes requires you to create a new subclass of ``Chute``. You must define a method ``run`` which accepts a single ``files`` argument (an array) and returns a new array of modified files. Besides ``run``, you can define any other methods you like on the new class.

.. code-block:: python

    from hellbox.chute import Chute

    class FilterFilesByExt(Chute):

        def __init__(self, *exts):
            self.exts = exts
      
        def run(self, files):
            return self._filter(files)

        def _filter(files):
            return [f for f in files if f.ext in self.exts]

You can then use your chute in your Hellfile as such:

.. code-block:: python
  
  with Hellbox('build') as task:
    task.read('*') >> FilterFilesByExt('ufo', 'txt') >> task.write('backup')

If your chute doesn't require arguments when initialized, you may prefer to define it with a function instead of a class. Using the ``@Chute.create`` function decorator makes a function definition act like a subclass of Chute:

.. code-block:: python

    from hellbox.chute import Chute

    @Chute.create
    def GenerateWOFF(files):
        # do something to files...
        return files
  
    with Hellbox('woff') as task:
        task.read('*.otf') >> GenerateWOFF() >> task.write('webfonts')

CLI
---

Hellbox comes with a command line tool ``hell`` which offers a thin layer over ``pip`` and ``virtualenv``. Using the CLI is optional, but makes working in isolation dead simple.

``hell init``

Sets up a new project by:

* Creating a new Python and ``pip`` install in the ``.hellbox`` directory
* Installing ``hellbox``
* Freezing all packages into ``requirements.txt``
* Creating a minimal ``Hellfile.py`` for defining tasks

``hell run {task}``

Runs the task defined in ``Hellfile.py``. Defaults to the task named `default`.

``hell install {package}``

Installs a package using ``pip`` into the project's Python installation and freezes ``requirements.txt``

``hell install``

Installs all packages in ``requirements.txt`` into the project's Python installation.

``hell uninstall {package}``

Uninstalls a package using ``pip`` from the project's Python installation and freezes ``requirements.txt``

``hell freeze``

Freezes all installed modules into ``requirements.txt``

``hell inspect``

Runs the ``Hellfile.py`` and displays the defined tasks:

.. code-block:: 
  
  Task: font
  ┗━ OpenFiles: '*.ufo'
     ┗━ GenerateOTF
        ┗━ WriteFiles: './otf'


.. _`install pip`: https://pip.pypa.io/en/latest/installing.html
