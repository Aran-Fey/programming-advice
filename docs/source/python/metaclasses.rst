
*****************************************
Metaclasses
*****************************************

Let me start by admitting that metaclasses are not useful very often. You can be a fine python programmer without ever using metaclasses. But at the same time, they're a very interesting concept and actually not too difficult to understand.

So with that out of the way: What are metaclasses?

The answer is: A metaclass is a class whose instances are classes. Or, to put it differently: The class of a class is a metaclass.

That's confusing, I know. But let me explain. It's a really simple concept, I swear.

Metaclasses are just OOP
========================

One of the things that make python so great is its consistency. What I mean by that is that it has relatively few core concepts, and many parts of the language are built on those concepts. Metaclasses are one example of this - they're the natural consequence of these two core principles:

1. Everything in python is an object.
2. Every object is an instance of a class.

The 2nd point is a fundamental part of `Object-Oriented Programming <https://en.wikipedia.org/wiki/Object-oriented_programming>`_ (OOP for short) and something you should already be familiar with. But for demonstration purposes, here's a small example of OOP::

    >>> # ['a', 'b'] is an instance of the list class
    >>> type(['a', 'b'])
    <class 'list'>
    >>> # We can create a new list object by calling the class
    >>> list('ab')
    ['a', 'b']

Like I said, that's all stuff you already know. But this is where the 1st point comes in: *Everything* in python is an object. That includes classes! The same things we just did with lists can also be done with classes::

    >>> # list is an instance of the type class
    >>> type(list)
    <class 'type'>
    >>> # We can create a new class by calling type.
    >>> # This requires 3 arguments:
    >>> # 1. The name of the class
    >>> # 2. A tuple of parent classes
    >>> # 3. The class's __dict__
    >>> type('MyClass', (), {})
    <class '__main__.MyClass'>

Neat, isn't it? Because classes are objects just like everything else, they behave in ways we're already familiar with. The term "metaclass" is something we use to refer to classes like ``type``, i.e. classes that generate other classes. That's the only difference between a regular class and a metaclass: Instantiating a regular class creates a new object, but instantiating a metaclass creates a new class. That's really all there is to it. A simple concept, don't you think?

Using metaclasses
============================

I already showed you one way of using metaclasses: Calling a metaclass with 3 arguments creates a new class. But there's another way: The ``class`` statement.

As you know, the ``class`` statement lets us create classes, like this::

    class Foo(Bar):
        x = 5

Behind the scenes, this actually just calls ``type`` with the 3 arguments ``'Foo'``, ``(Bar,)``, and ``{'x': 5}``. It's equivalent to this::

    Foo = type('Foo', (Bar,), {'x': 5})

You can specify a different metaclass, say :class:`abc.ABCMeta`, by passing in a ``metaclass`` keyword argument like so::

    class Foo(Bar, metaclass=abc.ABCMeta):
        x = 5

    # Equivalent to Foo = abc.ABCMeta('Foo', (Bar,), {'x': 5})

And if you pass in any other keyword arguments, they'll be forwarded to the metaclass::

    class Foo(Bar, metaclass=MyMeta, bar=True):
        x = 5

    # Equivalent to Foo = MyMeta('Foo', (Bar,), {'x': 5}, bar=True)

As far as I know, there is no metaclass in python's standard library that accepts these kinds of keyword arguments, but they can be useful if you write your own metaclass.

Writing custom metaclasses
============================

Python has one builtin metaclass: ``type``. Every class, metaclass or not, is an instance of ``type``. In order to write your own metaclass, all you have to do is subclass ``type``. That's how OOP works, after all. For example, here's a metaclass that adds a class attribute to each class and also implements a nicer ``__str__`` than the usual ``<class 'Foo'>``::

    class DemoMeta(type):
        def __init__(cls, name, bases, attrs):
            super().__init__(name, bases, attrs)

            cls.class_attribute = 'foo'

        def __str__(cls):
            return f'<{cls.__name__}>'

    class DemoClass(metaclass=DemoMeta):
        pass

    print(DemoClass.class_attribute)  # output: foo
    print(str(DemoClass))  # output: <DemoClass>

Writing a metaclass is really just like writing a regular class, except you have to inherit from ``type`` and if you write an ``__init__`` or ``__new__`` method you have to remember to add those 3 parameters that every metaclass needs. Everything else works as usual: Special methods like ``__init__`` and ``__str__`` do what they always do, ``super()`` works as it always does, etc. It's good practice to use the name ``cls`` instead of the usual ``self``, though.

One thing you have to be aware of is how attribute lookup works when metaclasses are involved. Firstly, dundermethods implemented in the metaclass only have an effect on its classes, not on instances of the classes::

    print(str(DemoClass))  # output: <DemoClass>

    demo_instance = DemoClass()
    print(str(demo_instance))
    # output: <__main__.DemoClass object at 0xdeadbeef>

And secondly, attributes of the metaclass can be accessed on the metaclass and its classes, but not on instances thereof::

    class DemoMeta(type):
        foo = 'foo'

    class DemoClass(metaclass=DemoMeta):
        pass

    DemoMeta.foo  # works
    DemoClass.foo  # works
    DemoClass().foo  # raises AttributeError

Now that you know how to write metaclasses, let me explain why you should think twice about doing so.

The problem with metaclasses
============================

To begin with, many programmers aren't familiar with metaclasses. Using them in your code will often make it harder to understand and less readable for most people. If possible, you should consider finding another solution. For example, a class decorator can oftentimes be used instead of a metaclass.

Metaclasses can also cause more concrete problems, though: Metaclass conflicts.

A metaclass conflict is what happens when a class inherits from 2 classes with incompatible metaclasses. "Incompatible" means that neither metaclass is a subclass of the other. For example, ``type`` and ``abc.ABCMeta`` are compatible, because ``ABCMeta`` is a subclass of ``type``::

    import abc

    class RegularClass: pass

    class AbstractClass(metaclass=abc.ABCMeta): pass

    class AlsoAnAbstractClass(RegularClass, AbstractClass): pass

    print(issubclass(abc.ABCMeta, type))  # True
    print(type(AlsoAnAbstractClass))  # <class 'abc.ABCMeta'>

Here, ``AlsoAnAbstractClass`` inherits from ``RegularClass`` (whose metaclass is ``type``) and ``AbstractClass`` (whose metaclass is ``ABCMeta``). Python realizes that ``ABCMeta`` is a subclass of ``type``, and so ``ABCMeta`` becomes the metaclass of ``AlsoAnAbstractClass``.

Now an example of incompatible metaclasses::

    class MyMeta(type): pass

    class MyClass(metaclass=MyMeta): pass

    class AbstractClass(metaclass=abc.ABCMeta): pass

    class ThisDoesntWork(MyClass, AbstractClass): pass
    # The class definition throws an exception:
    # TypeError: metaclass conflict: the metaclass of a derived class must
    # be a (non-strict) subclass of the metaclasses of all its bases

In this case, python can't choose whether ``ThisDoesntWork`` should be an instance of ``MyMeta`` or ``ABCMeta`` and throws an exception. Unfortunately, the only way to solve this problem is to create a new metaclass that inherits from both ``MyMeta`` and ``ABCMeta``::

    class MyAbstractMeta(MyMeta, abc.ABCMeta): pass

    class ThisWorks(MyClass, AbstractClass, metaclass=MyAbstractMeta):
        pass

So, remember: Just because you *can* use metaclasses doesn't mean you *should*. Use your newfound knowledge wisely.
