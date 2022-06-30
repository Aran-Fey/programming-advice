
#######################################
The python import system
#######################################

Python's import system is a common source of confusion for people who are new to the language. To make things worse, *a lot* of import-related advice on the internet is bad. There are tons of hacks and sketchy workarounds that may look like they "work", but actually turn your code base into a huge mess. So this is my attempt to teach you everything you need to know about imports in python.

The import statement
====================

Let's start with the purpose of imports. Imports allow us to load and use code that's written by other people, or is located in a different python script. By *importing* a module, we gain access to all functions, classes, variables, etc. of that module. Here's an example::

    # import the "os" module
    import os

    # now we can use the functions that are defined in that module
    print(os.getcwd())

Simple enough. Python imports the ``os`` module, and then automatically stores it in a variable with the same name as the module. If we want, we can tell python to store the module in a different variable with the ``as`` keyword::

    # import the "os" module and store it in the "foo" variable
    import os as foo

    print(foo.getcwd())  # works
    print(os.getcwd())   # throws NameError because there is no "os" variable

In both cases python creates a module object (that is, an instance of :class:`types.ModuleType`) and stores it in a variable. We can then access the module's contents through that module object.

There is another form of import which doesn't store the module in a variable at all, and instead creates variables for all the functions/classes/etc in the module: the ``from x import *`` style import. Here's an example of that::

    # import the "os" module and store all its functions in variables
    from os import *

    # now we can access the "os" module's functions directly:
    print(getcwd())     # works
    print(getlogin())   # also works
    print(os.getcwd())  # throws NameError because there is no "os" variable

The ``*`` tells python to create variables for *all* attributes of the module. This should be used sparingly. It's usually better to explicitly list all attributes you need::

    # import the "os" module and store the "getcwd" and "chdir" functions in variables
    from os import getcwd, chdir

    print(getcwd())     # works
    chdir('/home')      # also works
    print(getlogin())   # throws NameError because we didn't import this function

In all of these cases, we have imported the same module. The only thing that's different is how we access it and its attributes after the import.

The import system
=================



How files become modules
========================


