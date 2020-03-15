
#######################################
Writing maintainable code
#######################################

.. epigraph::

    A junior dev writes code that takes a senior dev to maintain. A senior dev writes code a junior dev could maintain.

Code often goes through changes throughout its life time, for example when you fix bugs or add features. You should always keep this in mind while programming, and try to write code that can easily accommodate changes. The less code you have to change in order to fix a bug or add a new feature, the better. That's what being maintainable means.

..
    There's a big overlap between readable code and maintainable code, because readability is pretty much a prerequisite for maintainability. Sometimes one can get in the way of the other, though. The sad truth about programming is that there's often no right way to write code - there are always tradeoffs. It's up to you to find a good balance between both.

..
    Unfortunately, maintainability often comes at a price. Sometimes writing maintainable code requires more development time than writing messy code. Other times maintainability can lead to more complex code, which gets in the way of readability. It's up to you to decide if these tradeoffs are worth it. If you're writing a quick-n-dirty script that you'll run one time and then delete, you don't need to concern yourself with maintainability. On the other hand, if you're part of a team that's working on a big project, maintainability should probably be your primary concern.

Like last time, I'll demonstrate how to achieve maintainability on a piece of poorly written code. It's a small round-based combat game where the players can choose between 2 classes with unique abilities. Our code looks like this::

    class Character:
        def __init__(self):
            self.health = 100
            self._health_potions = 3

        def get_health_potions(self):
            return self._health_potions

        def set_health_potions(self, potions):
            self._health_potions = potions

        def use_health_potion(self):
            if self.get_health_potions() > 0:
                self.set_health_potions(self.get_health_potions() - 1)
                self.health += 25
                print(f'Health Potion healed 25 hitpoints, you now '
                      f'have {self.health} hitpoints.')
            else:
                print('You have no Health Potions left.')

    class Mage(Character):
        def throw_fireball(self, enemy):
            enemy.health -= 25
            print(f'You deal 25 damage, your opponent now has '
                  f'{enemy.health} hitpoints.')

        def lesser_heal(self):
            self.health += 20
            print(f'You gain 20 health, you now have {self.health} '
                  f'hitpoints.')

    class Knight(Character):
        def heroic_strike(self, enemy):
            enemy.health -= 30
            print(f'You deal 30 damage, your opponent now has '
                  f'{enemy.health} hitpoints.')

        def first_aid(self):
            self.health += 15
            print(f'You gain 15 health, you now have {self.health} '
                  f'hitpoints.')

    def check_for_win(player1, player2):
        if player1.health <= 0:
            print('Player Two wins!')
            return True
        elif player2.health <= 0:
            print('Player One wins!')
            return True
        else:
            return False

    def assign_char(player_choice):
        if player_choice == 'Knight':
            return Knight()
        elif player_choice == 'Mage':
            return Mage()
        else:
            return 'Invalid'

    def action_menu(player, enemy):
        print('1. Use health potion')
        print('2. Attack')
        print('3. Heal')
        choice = input()

        if choice == '1':
            player.use_health_potion()
        elif choice == '2':
            if isinstance(player, Mage):
                player.throw_fireball(enemy)
            else:
                player.heroic_strike(enemy)
        elif choice == '3':
            if isinstance(player, Mage):
                player.lesser_heal()
            else:
                player.first_aid()
        else:
            print('You do nothing.')

    def play_game():
        print('Character Choices: Knight, Mage')
        player1 = assign_char(input('Player One, choose your character: '))
        player2 = assign_char(input('Player Two, choose your character: '))

        while not check_for_win(player1, player2):
            print('Player 1')
            action_menu(player1, player2)
            if check_for_win(player1, player2):
                break

            print('Player 2')
            action_menu(player2, player1)

    play_game()

In order to figure out why that code is bad, let's think about how much effort it would take to make some changes to our little game. Here are some ideas for new features, each with a list of changes that it would require:

* Adding a 3rd playable class

  1. Create a new subclass of ``Character``
  2. Add the new class to the ``assign_char`` function
  3. Add the new class to the ``action_menu`` function
  4. Add the new class to the ``print`` call in the ``play_game`` function

  Because of the way the ``skill_menu`` function is implemented, the new class would also have to have exactly 1 offensive skill and 1 healing skill. If we wanted our class to have 2 offensive skills, we'd have to completely rewrite the ``skill_menu`` function.

* Adding an AI opponent

  1. Implement a simple AI
  2. Add a menu that lets the player choose between an AI or a human opponent
  3. Every time player 2 takes their turn, check if they're an AI and either call ``skill_menu`` or let the AI choose what to do.

  The biggest problem here would be implementing the AI. Even a stupid AI that picks an action at random would have to know what class it's playing and what abilities that class has. So every time a new class is added, the AI has to be updated as well.

* Allowing more than 2 players

  1. Rewrite the ``check_for_win`` function
  2. Rewrite the character selection in the ``play_game`` function
  3. Rewrite the ``skill_menu`` menu loop in the ``play_game`` function

As you can see, implementing any of these features would require changes in multiple parts of the code. That's a sign of spagetthi code. Ideally, each feature should be a self-contained unit. The less code you have to rewrite, the less likely you are to mess something up and create bugs. So let's start improving the code.

Improvement #1: Don't use Java-style getters and setters
========================================================

Many people who learn python as a secondary language make the mistake to write Java-style accessor methods like these::

    def get_health_potions(self):
        return self._health_potions

    def set_health_potions(self, potions):
        self._health_potions = potions

In Java, these serve a purpose: `Data Hiding <https://en.wikipedia.org/wiki/Information_hiding>`_. The idea is that nobody has direct access to the object's attributes; you can only interact with the attribute through the accessor methods. This gives the class full control over what happens when an attribute is accessed or modified.

In python this is not necessary because we have :class:`property`. The correct way to implement accessors in python is this::

    @property
    def health_potions(self):
        return self._health_potions

    @health_potions.setter
    def health_potions(self, potions):
        self._health_potions = potions

This disguises the accessor functions as normal attribute access. So instead of having to write gross code like this::

    self.set_health_potions(self.get_health_potions() - 1)

we can write pretty code like this::

    self.health_potions -= 1

The best part is that since it can be used just like a regular attribute, we don't have to implement accessors unless we actually need them. Because a property looks just like a regular attribute to the outside world, we can turn a regular attribute into a property without breaking anyone's code. So if you don't need accessors, don't write them.

With that in mind, we can rewrite our ``Character`` class to this::

    class Character:
        def __init__(self):
            self.health = 100
            self.health_potions = 3

        def use_health_potion(self):
            if self.health_potions > 0:
                self.health_potions -= 1
                self.health += 25
                print(f'Health Potion healed 25 hitpoints, you now '
                      f'have {self.health} hitpoints.')
            else:
                print('You have no Health Potions left.')

Improvement #2: Don't repeat yourself
=====================================

We already learned that writing the same code twice is a bad idea, and yet our code still makes that mistake quite a few times. Let's change that and make our code `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_.

Don't hard-code values, use constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In every single character ability, the amount of damage dealt to the enemy or health restored to your own character is used twice - once to update the character's health, and once to print a status message::

    def throw_fireball(self, enemy):
        enemy.health -= 25
        print(f'You deal 25 damage, your opponent now has '
              f'{enemy.health} hitpoints.')

If we ever want to change this value, we have to change it in two places. That can be avoided by storing the value in a variable::

    def throw_fireball(self, enemy):
        dmg = 25
        enemy.health -= dmg
        print(f'You deal {dmg} damage, your opponent now has '
              f'{enemy.health} hitpoints.')

Don't half-ass your functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take a look at how the code uses the ``assign_char`` and ``action_menu`` functions. Every time one of those functions is called, the code actually does something else first. In case of ``assign_char``, we always ask for user input first::

    player1 = assign_char(input('Player One, choose your character: '))
    player2 = assign_char(input('Player Two, choose your character: '))

And in case of ``action_menu``, we always print a message first::

    print('Player 1')
    action_menu(player1, player2)

    ...

    print('Player 2')
    action_menu(player2, player1)

If we're always going to do a specific thing before calling a function, then why don't we make the function do that thing for us instead?

Use more loops
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the ``play_game`` function, we do similar things for both players: First we ask both players to choose their character, and then we repeatedly let each player perform an action and then check if someone has won the game. We're always repeating the same thing for both players. Instead of copying every piece of code for each player, we can write a loop that takes care of each player in turn. In order to do that, we'll get rid of the ``player1`` and ``player2`` variables and replace them with a list of players.

After implementing all of these improvements, the code looks like this::

    class Character:
        def __init__(self):
            self.health = 100
            self.health_potions = 3

        def use_health_potion(self):
            if self.health_potions > 0:
                heal = 25
                self.health_potions -= 1
                self.health += heal
                print(f'Health Potion healed {heal} hitpoints, you now '
                      f'have {self.health} hitpoints.')
            else:
                print('You have no Health Potions left.')

    class Mage(Character):
        def throw_fireball(self, enemy):
            dmg = 25
            enemy.health -= dmg
            print(f'You deal {dmg} damage, your opponent now has '
                  f'{enemy.health} hitpoints.')

        def lesser_heal(self):
            heal = 20
            self.health += heal
            print(f'You gain {heal} health, you now have {self.health} '
                  f'hitpoints.')

    class Knight(Character):
        def heroic_strike(self, enemy):
            dmg = 30
            enemy.health -= dmg
            print(f'You deal {dmg} damage, your opponent now has '
                  f'{enemy.health} hitpoints.')

        def first_aid(self):
            heal = 15
            self.health += heal
            print(f'You gain {heal} health, you now have {self.health} '
                  f'hitpoints.')

    def check_for_win(player_names, player_characters):
        if player_characters[0].health <= 0:
            print(f'{player_names[1]} wins!')
            return True
        elif player_characters[1].health <= 0:
            print(f'{player_names[0]} wins!')
            return True
        else:
            return False

    def assign_char(player_name):
        player_choice = input(f'{player_name}, choose your character: ')

        if player_choice == 'Knight':
            return Knight()
        elif player_choice == 'Mage':
            return Mage()
        else:
            return 'Invalid'

    def action_menu(player_name, player, enemy):
        print(player_name)
        print('1. Use health potion')
        print('2. Attack')
        print('3. Heal')
        choice = input()

        if choice == '1':
            player.use_health_potion()
        elif choice == '2':
            if isinstance(player, Mage):
                player.throw_fireball(enemy)
            else:
                player.heroic_strike(enemy)
        elif choice == '3':
            if isinstance(player, Mage):
                player.lesser_heal()
            else:
                player.first_aid()
        else:
            print('You do nothing.')

    def play_game():
        player_names = ['Player One', 'Player Two']
        player_characters = []

        print('Character Choices: Knight, Mage')
        for player_name in player_names:
            character = assign_char(player_name)
            player_characters.append(character)

        while True:
            # let each player take their turn
            for player_name in player_names:
                # find the player character and the enemy character
                if player_name == player_names[0]:
                    player, enemy = player_characters
                else:
                    enemy, player = player_characters

                action_menu(player_name, player, enemy)

                if check_for_win(player_names, player_characters):
                    return

    play_game()

But what's this? The ``play_game`` function is suddenly much longer and much more complicated than before! Especially that ``while True:`` loop is quite a mess now.

This is actually a pretty common thing. Trying to make code more maintainable often makes it more complex, and thus less readable. Which is kind of an oxymoron, because how can code that's hard to read be easy to maintain? Unfortunately, that's something we have to live with. There isn't always a perfect solution. It's up to you to decide if the tradeoffs are worth it. Finding the best solution is what's really hard about programming.

For now, we'll leave the code like this, despite the mess in ``play_game``. Some of the upcoming changes will let us make it a little better.

..
    In this particular case though, we can actually do something about the mess in ``play_game``.

Improvement #3: Error handling with exceptions
========================================================



Improvement #2: Encapsulation
========================================================

`Encapsulation <https://en.wikipedia.org/wiki/Encapsulation_(computer_programming)>`_ means bundling data together

Improvement #2: Abstraction and interfaces
========================================================

One of the reasons why the game's code is messy is because the ``Character`` subclasses ``Mage`` and ``Knight`` are too different from each other. ``Mage`` has the two abilities ``throw_fireball`` and ``lesser_heal``, whereas ``Knight`` has ``heroic_strike`` and ``first_aid``. Because of these differences, the ``action_menu`` function has to check what kind of character you're playing to figure out which of these functions it has to call.

The solution to this problem is to make all ``Character`` subclasses implement the same `interface <https://en.wikipedia.org/wiki/Interface_(computing)>`_.

One way to do that is to rename ``throw_fireball`` and ``heroic_strike`` to ``attack``, and ``lesser_heal`` and ``first_aid`` to ``heal``. That way both classes would have the same methods, which eliminates the need to check what kind of character you're playing.

That's a good and easy solution. The only problem with it is that it forces each character to have one offensive ability and one healing ability. So if you're planning to add characters that don't have a healing ability, you have to approach the problem differently.

That approach is `abstraction <https://en.wikipedia.org/wiki/Abstraction_principle_(computer_programming)>`_, more specifically `generalization <https://en.wikipedia.org/wiki/Generalization>`_. Currently, each ability is represented by a function. Offensive abilities are functions that require a ``target`` argument, and healing abilities are functions with no arguments. The problem with this interface is two-fold:

1. Not every function in the class represents an ability
2. It's hard to tell apart offensive abilities and healing abilities

To solve these problems, we'll stop representing abilities as methods and implement them as instances of an ``Ability`` class instead. We'll also create the subclasses ``TargetedAbility`` and ``UntargetedAbility`` to distinguish offensive abilities from healing abilities. Each character will have a list of abilities that it can use.

But we can take it even further than that: Just like abilities, health potions are also something the player can *use*. So we're going to add an ``Action`` class that represents any kind of action the player can perform. The ``UntargetedAction`` subclass will have a ``do(character)`` method, which takes the character that's performing the action as input. The ``TargetedAction`` subclass's ``do`` method will additionally require a ``target`` argument.

::

    class Action:
        def __init__(self, name):
            self.name = name

    class UntargetedAction(Action):
        def do(self, character):
            raise NotImplementedError

    class TargetedAction(Action):
        def do(self, character, target):
            raise NotImplementedError

    class SelfHealAction(UntargetedAction):
        def __init__(self, heal, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.heal = heal

        def do(self, character):
            character.health += self.heal
            print(f'{self.name} healed {self.heal} hitpoints, you now '
                  f'have {character.health} hitpoints.')

    class UseHealthPotion(SelfHealAction):
        def __init__(self):
            super().__init__(25, 'Health Potion')

        def do(self, character):
            if character.health_potions > 0:
                character.health_potions -= 1
                super().do(character)
            else:
                print(f'You have no {self.name}s left.')

    class DamageAbility(TargetedAction):
        def __init__(self, damage, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.damage = damage

        def do(self, character, target):
            target.health -= self.damage
            print(f'You deal {self.damage} damage, your opponent now '
                  f'has {target.health} hitpoints.')

    class Character:
        def __init__(self):
            self.health = 100
            self.health_potions = 3
            self.actions = [UseHealthPotion()]

    class Mage(Character):
        def __init__(self):
            super().__init__()

            self.actions += [
                DamageAbility(25, 'Fireball'),
                SelfHealAction(20, 'Lesser Heal')
            ]

    class Knight(Character):
        def __init__(self):
            super().__init__()

            self.actions += [
                DamageAbility(30, 'Heroic Strike'),
                SelfHealAction(15, 'First Aid')
            ]

    def check_for_win():
        if player_characters[0].health <= 0:
            print(f'{player_names[1]} wins!')
            return True
        elif player_characters[1].health <= 0:
            print(f'{player_names[0]} wins!')
            return True
        else:
            return False

    def assign_char(player_name):
        player_choice = input(f'{player_name}, choose your character: ')

        if player_choice == 'Knight':
            return Knight()
        elif player_choice == 'Mage':
            return Mage()
        else:
            return 'Invalid'

    def action_menu(player_name, player, enemy):
        print(player_name)
        for i, action in enumerate(player.actions, 1):
            print(f'{i}. {action.name}')

        choice = input()
        try:
            i = int(choice) - 1
            action = player.actions[i]
        except (ValueError, IndexError):
            print('You do nothing.')
        else:
            if isinstance(action, TargetedAction):
                action.do(player, enemy)
            else:
                action.do(player)

    def play_game():
        global player_names, player_characters
        player_names = ['Player One', 'Player Two']
        player_characters = []

        print('Character Choices: Knight, Mage')
        for player_name in player_names:
            character = assign_char(player_name)
            player_characters.append(character)

        while True:
            # let each player take their turn
            for player_name in player_names:
                # find the player character and the enemy character
                if player_name == player_names[0]:
                    player, enemy = player_characters
                else:
                    enemy, player = player_characters

                action_menu(player_name, player, enemy)

                if check_for_win():
                    return

    play_game()

This has multiple advantages:

* Since each character has a list of actions they can perform, the ``action_menu`` function has become a lot simpler.
* Healing abilities and health potions have a lot in common - the only difference is that using a health potion removes it from the player's inventory. The code that's responsible for restoring health is now implemented in ``SelfHealAction`` and used by both healing abilities as well as health potions.


Improvement #4: Generalize instead of making assumptions
========================================================

The code for our game was written based on the premise that there are two players fighting against each other. This assumption that there are always exactly two players has manifested in various different parts of the code:

1. In the original code, the ``play_game`` function lets exactly 2 people choose their character, and then it let exactly 2 players take their turns.
2. The ``check_for_win`` function checks the health of exactly two players, and if one is dead then it declares the other one the winner.
3. If a player uses an offensive ability, the game automatically selects the other player as the target.

Part of the reason why the loop in ``play_game`` became so messy is because
