
###############################
Project Structure for beginners
###############################

Many people run into problems once their projects grow beyond just a single python script. When you work with multiple files, they need to be able to import each other - and python's import system is probably one of its most confusing aspects.

Structuring your project properly helps avoid many of these problems. Unfortunately, the proper way to do this is pretty involved and not very suitable for beginners. The project structure I will be recommending here will work well enough for most beginners, but if you're planning to publish and distribute your project, you should look into how to create a `pyproject.toml <https://www.python.org/dev/peps/pep-0518/>`_ file and the `poetry <https://python-poetry.org/docs/>`_ project.

.. note::
    I will not be covering the import system in detail. If you aren't familiar with it yet, you may want to read up on the `import statement <https://docs.python.org/3/reference/simple_stmts.html#grammar-token-import-stmt>`_ or the `import system <https://docs.python.org/3/reference/import.html>`_ in general first.

Pros and Cons of this setup
===========================

Advantages:

* It's simple.
* Starting the program is easy and intuitive (for programmers) - all you need to do is execute a python script.

Disadvantages:

* It's not suitable for proper packaging and publishing. (This doesn't take much effort to fix, though.)
* The user is responsible for installing all required dependencies.
* You won't be able to import a project in another project. (At least not without modifying your :envvar:`PYTHONPATH` or :data:`sys.path`.)

The Project Structure
=====================

The file hierarchy
~~~~~~~~~~~~~~~~~~

There are two key points to making the imports in your project work correctly:

1. Strict separation of files that are *imported* and files that are *executed* by the user.
2. Putting the importable files in a place where python can find them.

This can be achieved by organizing your files like this::

    project-name/
        package_name/
            __init__.py
            importable_file1.py
            importable_file2.py
            ...
        executable-file1.py
        executable-file2.py
        ...

The names are only placeholders, of course (except for ``__init__.py``) - what matters is the structure.

All of the importable files are grouped in the ``package_name`` `package <https://docs.python.org/3/tutorial/modules.html#packages>`_, and all executable files are on the same level as ``package_name``. When a python script is executed by the user, the location of that script is automatically added to python's module search path (:data:`sys.path`), so all of the executable files will be able to import ``package_name`` (and its submodules).

The ``__init__.py`` is required for python to recognize ``package_name`` as a package - its contents are not important, what matters is that it exists. You can leave it completely empty if you want, or you can learn more about it `here <https://stackoverflow.com/questions/448271/what-is-init-py-for>`_.

Of course, you don't necessarily have to put all your importable scripts directly into the ``package_name`` folder. You're free to organize your code into sub-packages, if you like.

If you need any other files (e.g. ``README``, ``LICENSE``) or folders (e.g. ``docs``, ``tests``, ``.git``), they should be placed directly in the ``project-name`` directory.

Imports
~~~~~~~

Because all importable files are now submodules of ``package_name``, your imports will have to look like this::

    # importing the whole file
    import package_name.importable_file1
    # or
    from package_name import importable_file1
    
    # importing only specific things from a file
    from package_name.importable_file1 import MyClass, my_function

Inside of ``package_name`` you can also use `relative imports <https://docs.python.org/3/reference/import.html#package-relative-imports>`_, if you're familiar with those.

And just to make this extra clear: You should never import any of the executable files. Everything you want to import should be somewhere in ``package_name``.

Configuring your IDE
====================

Unfortunately some IDEs don't support this setup out of the box. You'll be able to successfully run your code from the command line or even by double-clicking a ``.py`` file, but if you're using an IDE it might get in the way and break things. (I'm looking at you, PyCharm.)



Common mistakes
===============

For completeness' sake, I'm going to explain some of the problems that beginners often run into. This is only here to help people who had problems setting up their project understand what they were doing wrong. You can skip this part if you're not interested.

Using relative imports in executable files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say you have an executable file ``executable_file.py`` with a relative import like this::

    from .importable_file import my_function
    
This will crash with an ``ImportError``. Relative imports only work inside a package, and python doesn't consider ``executable_file.py`` to be a part of any package. When a file is executed directly by the user, python assigns that file the name "__main__" and thinks of it as its own module. That's why every file that can be executed by the user must use absolute imports.

Importing the file that the user executed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the file that was executed by the user is involved in a circular import, really strange things can happen. For example, if you have an ``importable_file.py`` like this::

    import executable_file

    def is_foo(obj):
        print(isinstance(obj, executable_file.Foo))

and an ``executable_file.py`` like this::

    import importable_file

    class Foo:
        pass

    print('Hello from executable_file.py')

    if __name__ == '__main__':
        importable_file.is_foo(Foo())

The output will be this::

    Hello from executable_file.py
    Hello from executable_file.py
    False

Not only was ``executable_file.py`` executed twice, but somehow python can't even recognize a ``Foo`` object as an instance of ``Foo``!

The reason for this is a little complicated.

Python assigns each module a name, which is usually the name of the file. For example, if you do ``import importable_file``, python executes ``importable_file.py`` and registers that module under the name "importable_file". If you do ``import importable_file`` a second time, python realizes that a module named "importable_file" already exists and simply returns that module without executing ``importable_file.py`` again.

Now, the problem is that when a file is executed by the user, python assigns that file the name "__main__". So even though the file is named "executable_file.py", python only knows it as "__main__". When ``import executable_file`` is executed, python can't find a module named "executable_file", and decides to create that module by executing the code in ``executable_file.py``. That's why ``executable_file.py`` is executed twice.

In the end, we have a "__main__" module and an "executable_file" module. Even though they were created from the same file, python still considers them two different modules. And that applies to the contents of those modules as well: As far as python is concerned, ``__main__.Foo`` is not the same class as ``executable_file.Foo``. That explains why ``isinstance(obj, executable_file.Foo)`` returns ``False`` - ``obj`` is an instance of ``__main__.Foo``, not ``executable_file.Foo``.

Never ever import a file that's supposed to be executed by the user.

Directly importing a submodule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say you have a package like this::

    package_name/
        executable_file.py
        importable_file1.py
        importable_file2.py

``importable_file1.py`` contains this code::

    from .importable_file2 import my_function

And ``executable_file.py`` contains an import like this::

    import importable_file1

This code will crash with an ``ImportError``, and it's all because of the ``import importable_file1``. The problem is that this import tells python to import a module named "importable_file1", when in reality we're trying to import the module "package_name.importable_file1". Because of this incorrect import, python creates a new "importable_file1" module that is *not* a submodule of ``package_name``, and that causes the relative imports in ``importable_file1.py`` to crash.

The only reason why the incorrect import works in the first place is because ``executable_file.py`` is in the same directory as ``importable_file1.py``, so this problem can be avoided by moving ``executable_file.py`` out of ``package_name``. That way you'll be forced to use the correct ``from package_name import importable_file1`` import.
