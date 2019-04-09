Hellbox
=======

.. image:: https://travis-ci.org/hellboxpy/hellbox.svg?branch=master
    :target: https://travis-ci.org/hellboxpy/hellbox

Hellbox is a modular, editor-agnostic build system designed for font development. Hellbox is similar to some "Flow-based Programming" environments, consisting of a system of chained blackbox components.

**Hellbox is in the early stages of development. This document is more of a roadmap than documentation of the current implementation. Expect API changes without notice until v1.0.**

Goals
-----

* **Consistency** Hellbox tasks don't take arguments by design, favoring consistent task output
* **Modularity** Hellbox packages should be resuable and composable, while maintaining flexibility for custom workflows
* **Isolation** Hellbox tasks and packages are version locked and isolated from other projects and Python installations

Overview
--------

Hellbox aims to provide both an environment and framework for defining build pipelines.

Hellbox tasks are composed of "chutes" — modules that perform a single operation over one or more files. Chutes are connected together using the ``>>`` operator, linking the output of one chute to the input of the next.

.. code-block:: python

    from hellbox import Hellbox
    from hellbox_generate_otf import GenerateOtf

    with Hellbox("build") as task:
        task.describe("Builds .otf files from .ufo source")
        task.read("*.ufo") >> GenerateOtf() >> task.write("./otf")

With the above configuration, running ``hell run build`` will generate OTF files from all of the UFO sources, and write them to the ``otf`` directory.

Installation
------------

First `install hell`_, a CLI for managing hellbox projects. Then run ``hell init`` inside of your project (or ``hell install`` inside of an existing hellbox-enabled project).

This will set up a new virtual environment with Python 3 using `pipenv`, create a ``Hellfile.py`` for defining tasks, and install the ``hellbox`` library itself.

.. _`install hell`: https://github.com/hellboxpy/hell#installation

Chutes
------

There are two ways of defining a Hellbox chute, depending on the complexity and amount of configuration required.

The basic setup for defining your own chutes requires you to create a new subclass of ``Chute``. You must define a method ``run`` which accepts a single ``files`` argument (an array) and returns a new array of modified files. Besides ``run``, you can define any other methods you like on the new class.

.. code-block:: python

    from hellbox.chute import Chute

    class FilterFilesByExt(Chute):

        def __init__(self, *extensions):
            self.extensions = extensions

        def run(self, files):
            return [f for f in files if f.extension in self.extensions]

You can then use your chute in your Hellfile as such:

.. code-block:: python

  with Hellbox("backup") as task:
      task.read("build/*") >> FilterFilesByExt("otf", "txt") >> task.write("backup")

If your chute doesn't require arguments when initialized, you may prefer to define it with a function instead of a class. Using the ``@Chute.create`` function decorator makes a function definition act like a subclass of Chute:

.. code-block:: python

    from hellbox.chute import Chute

    @Chute.create
    def GenerateWoff2(files):
        # do something to files...
        return files

    with Hellbox("webfonts") as task:
        task.read("build/*.ttf") >> GenerateWoff2() >> task.write("webfonts")

CLI
---

Hellbox comes with a command line tool `hell`_ which offers a thin layer over ``pipenv``. Using the CLI is highly recommended, as it makes working in isolation dead simple.

.. _`hell`: https://github.com/hellboxpy/hell/blob/master/README.md#installation

Development
-----------

Install development dependencies with ``make``. Run tests with ``make test``.
