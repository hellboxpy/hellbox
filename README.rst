Hellbox
=======

Hellbox is a modular, editor-agnostic build system designed for font development.

.. code-block:: python
  
  from hellbox import Hellbox
  
  Hellbox.autoimport()
  
  with Hellbox('build') as task:
      task.source('*.ufo').to(GenerateOTF()).to(Hellbox.write('./otf'))

  Hellbox.default = 'build'

**Hellbox is in the early stages of development. This document is more of a roadmap than documentation of the current implementation. Expect API changes without notice until v0.1.**

Installation
------------

First `install pip`_ (if not present), then run:

``pip install git+git://github.com/jackjennings/hellbox.git``

Goals
-----

* **Consistency** Hellbox tasks don't take arguments by design, favoring consistent task output.
* **Modularity** Hellbox packages should be resuable and composable, while maintaining flexibility for bespoke workflows.
* **Isolation** Hellbox tasks and packages are version locked and isolated from other Python installations.

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

Plugins
-------

``TODO``


.. _`install pip`: https://pip.pypa.io/en/latest/installing.html
