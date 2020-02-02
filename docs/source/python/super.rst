
*****************************************
Understanding python's ``super`` function
*****************************************

The :func:`super` function is one of python's least understood (and most misunderstood) features¸ which is a shame because it can be a very powerful tool if you know how to use it.

In order to clear up any misunderstandings you might have, I'll try to explain ``super`` in as much detail as possible.
First, let's talk about its purpose: ``super`` can be used to access attributes or methods of a parent class from within a child class, for example like this::

    class Parent:
        def __init__(self):
            self.x = 0

    class Child(Parent):
        def __init__(self):
            # call the parent constructor
            super().__init__()

            self.y = 1

Here we used ``super`` to call the parent class's constructor, like any good child class should do.

But it's not really correct to say that ``super`` lets you access attributes of your *parent* class. It's a bit more complicated than that. The truth is that ``super`` operates on a class's `Method Resolution Order <https://docs.python.org/3/glossary.html#term-method-resolution-order>`_ (MRO for short). The MRO is a list of classes that dictates the order in which python searches those classes for attributes and methods. For example, the MRO of ``Child`` looks like this::

    >>> Child.__mro__
    (<class '__main__.Child'>, <class '__main__.Parent'>, <class 'object'>)

This means that whenever you access an attribute of ``Child``, python first looks for that attribute in ``Child``'s namespace, then - if it can't find the attribute there - ``Parent``'s namespace, and finally ``object``'s namespace.

``super`` does the same thing, except it skips some of the classes in the MRO. When we call ``super()`` with no arguments like we did earlier, it's actually a shorthand for ``super(__class__, self)`` (where ``__class__`` is the class the method is defined in). So in the example above, ``super()`` is equivalent to ``super(Child, self)``. This ``super(Child, self).__init__()`` skips looking for ``__init__`` in ``Child``'s namespace and only starts its search at ``Parent``. That's where it finds ``Parent.__init__`` and calls it, automagically passing in ``self`` as the first argument so you don't have to.

Now, this is where it gets interesting. You probably assumed that ``super(Class, instance)`` operates on the MRO of ``Class``, right? Well, you're in for a surprise - it actually operates on the MRO of ``type(instance)``! Because of the way the MRO works in python, this can lead to some surprises if multiple inheritance is involved.


The MRO and Multiple Inheritance
================================

We've already learned that the MRO is a list of classes that dictates how python searches for class attributes and methods. This is easy to understand if the class has only one parent class - in that case the MRO is simply the parent's MRO with the child class inserted at the front::

    class Parent:
        pass

    class Child(Parent):
        pass

    print(Parent.__mro__)
    # (<class '__main__.Parent'>, <class 'object'>)

    print(Child.__mro__)
    # (<class '__main__.Child'>, <class '__main__.Parent'>, <class 'object'>)

But what if a class has more than one parent? Which parent will come first in the MRO? And what about the parents' parents?

The answer is that python uses an algorithm called `C3 linearization <https://en.wikipedia.org/wiki/C3_linearization>`_ to generate the MRO. Here's a short summary of it:

1. If a class has multiple parents, like ``class Child(Parent1, Parent2)``, the order of the parents relative to each other will stay the same in the MRO - i.e. ``Parent1`` will appear before ``Parent2``.
2. A child class will appear in the MRO before all of its parent classes.

Here's an example of that::

    class Foo:
        def __init__(self):
            print('foo')

            super().__init__()

    class Bar:
        def __init__(self):
            print('bar')

    class FooBar(Foo, Bar):
        def __init__(self):
            super().__init__()

    print(FooBar.__mro__)
    # (<class '__main__.FooBar'>,
    #  <class '__main__.Foo'>,
    #  <class '__main__.Bar'>,
    #  <class 'object'>)

You can see that ``FooBar`` appears first in the MRO, before its parents. ``Foo`` appears before ``Bar``, because ``FooBar`` listed ``Foo`` as its first parent and ``Bar`` as its 2nd parent. And last but not least, both ``Foo`` and ``Bar`` appear before ``object``, because both are subclasses of ``object``.

Compare this with the MRO of ``Foo``: Even though ``Foo``'s MRO is ``(<class '__main__.Foo'>, <class 'object'>)``, in ``FooBar``'s MRO ``Bar`` appears *between* ``Foo`` and ``object``! And because ``super`` operates on the MRO of the instance, the ``super().__init__()`` in ``Foo`` will behave differently depending on whether ``self`` is an instance of ``Foo`` or ``FooBar``::

    Foo()  # output: foo
    FooBar()  # output: foo bar

Remember, ``super(Foo, self)`` looks at the MRO of ``type(self)`` and skips everything up to ``Foo``. When ``self`` is an instance of ``Foo``, the ``super().__init__()`` in ``Foo`` calls ``object.__init__``. But when ``self`` is an instance of ``FooBar``, it calls ``Bar.__init__``.

That's the cool thing about ``super``: It can do different things depending on the type of the instance. But you're probably wondering: What is that useful for?

Applications of ``super``
=========================

Mixins
~~~~~~

A `mixin <https://en.wikipedia.org/wiki/Mixin>`_ is a class that adds features to your class if you inherit from it. Here's an example where we use a mixin to create all kinds of things that can produce sounds::

    class NoiseMixin:
        def __init__(self, *args, noise, **kwargs):
            super().__init__(*args, **kwargs)

            self.noise = noise

        def make_noise(self):
            print(self.noise)

    class Animal:
        def __init__(self):
            self.is_alive = True

    class Turtle(Animal):
        pass

    class Dog(NoiseMixin, Animal):
        pass

    class Train(NoiseMixin):
        pass

    lord_voldetort = Turtle()
    rex = Dog(noise='bark')
    spot = Dog(noise='whimper')
    thomas = Train(noise='choo choo')

Without ``super`` we would have a problem implementing ``NoiseMixin``'s ``__init__`` method here. ``NoiseMixin.__init__`` would override any other ``__init__``, and because of that, instantiating a ``Dog`` would never call ``Animal.__init__``.


Cooperative multiple inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In cooperative multiple inheritance you write a few classes that each implement a small set of features, and then inherit from those classes to create various different combinations of features. It's kind of like a bunch of mixins that all work together.
As an example, think of enemy units in a tower defense game. Some units might walk on the ground while others fly. Some units might use ranged weapons while others use melee weapons. In your code, you could write a class for each type of unit and then combine them however you need to::

    # abstract base class for all units
    class Unit:
        def __init__(self, attack, health):
            self.attack = attack
            self.health = health

    # cooperative base classes
    class GroundUnit(Unit):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.affected_by_traps = True

    class FlyingUnit(Unit):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.affected_by_traps = False

    class MeleeUnit(Unit):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.ranged = False

    class RangedUnit(Unit):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.ranged = True

    # some actual units
    class DwarvenWarrior(GroundUnit, MeleeUnit):
        pass

    class AngelicArcher(FlyingUnit, RangedUnit):
        pass

    gimli = DwarvenWarrior(5, 20)

Once again we used ``super`` to chain all our ``__init__`` methods together.
