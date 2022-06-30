
***********************
Writing readable code
***********************

.. epigraph::

   Any fool can write code that a computer can understand. Good programmers write code that humans can understand.

   -- Martin Fowler

Being easy to understand is one of the most important qualities of good code. Unfortunately, this is something that takes beginners a long time to figure out. This is because they never have to read complicated code - the only code they read are short snippets from tutorials and their own code. Reading your own code is easy, especially when it only takes a few days or maybe a week to write. But when you've worked on a program for months or even years and it has thousands of lines of code, being able to understand the code you wrote a long time ago becomes exponentially more difficult and important, especially if you're working in a team.

Beginners write code for computers. Experienced devs write code for humans.

See, computers need very specific instructions to understand what we want them to do. Instructions like "set this variable to 0" or "add 1 to this variable". But for a human it's hard to understand what that long list of detailed instructions actually *does*. We humans don't want to concern ourselves with details, we want to understand the big picture. All those detailed instructions that tell the computer *how* to do its job are irrelevant to us. We just want to know *what* the code is doing.

In order to help you understand just how important writing readable code is, let's perform a little experiment. I'm going to show you a really bad piece of python code and you'll try to figure out what it does. There's nothing complicated about it, it uses simple syntax that even a beginner can understand. Here we go, give it your best shot::

    my_dict = {
        'Bandage': 5,
        'Health Potion': 7
    }

    def my_func(itms, m):
        count = 0

        for i in itms:
            count += my_dict[i] * itms[i]

        return m - count

How did it go? Could you figure out what the ``my_func`` function does? Was it easy? How much time did you spend on it? It's only 11 lines of code, so you must've figured it out pretty quickly, right?

Now, for comparison, let's try that again with the same piece of code, except this time all the variables have more meaningful names. Round two::

    ITEM_PRICES = {
        'Bandage': 5,
        'Health Potion': 7
    }

    def calc_change(item_quantities, money):
        total_price = 0

        for item in item_quantities:
            total_price += ITEM_PRICES[item] * item_quantities[item]

        return money - total_price

How did you do this time? Do you have a better idea of the function's purpose? How long did it take you to figure it out?

This one was a lot easier, wasn't it?

I hope this little experiment made it clear just how big the difference between good and bad code is. Even if it's just 11 lines of simple code, an easy improvement like using better variable names can have a huge impact.

Common mistakes and how to fix them
===================================

In this section we'll take a bad piece of code and gradually improve it. The program we'll be using is a simple Rock-Paper-Scissors game, a common beginner project. The game asks each player to choose a hand and displays the winner. After 3 rounds, the game ends and asks the player if they want to play again.

We'll start with this code::

    def Outcome():
        # check all combinations
        if c1 == c2:
          print('Tie!')
        elif ((c2== 'Rock' and c1 == 'Paper') or
              (c2== 'Paper' and c1 =='Scissors') or
              (c2== 'Scissors' and c1 == 'Rock')):
            print('Player 1 wins!' )
        elif ((c1== 'Rock' and c2 == 'Paper') or
              (c1== 'Paper' and c2 =='Scissors') or
              (c1== 'Scissors' and c2 == 'Rock')):
            print ('Player 2 wins!')

    while True:
        n = 0
        while n<3:
            while True:
                # ask for user input
                c1 = input ("Player 1: Rock, Paper, or Scissors? ")
                if c1 == 'Rock' or c1 == 'Paper' or c1 =='Scissors' :
                  break  # check passed
                print("Invalid input")
            while True:
                c2 = input("Player 2: Rock, Paper, or Scissors? ")
                if c2 == 'Rock' or c2=='Paper' or c2 == 'Scissors':
                    break
                print("Invalid input")
            n += 1  # increment counter by 1
            Outcome()  # call outcome function
        Game = input("Would you like to play again? ")
        if Game == 'n' or Game == 'N'or Game == 'no' or Game == 'No':
          break

This code works; you can try it if you want. But it's not *good* code, so let's change that.

Improvement #1: Consistent formatting and PEP 8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing you'll notice when you look at this code is that it's a giant block of text. Every single line is full of code, except
the one after the function definition. Just looking at this feels suffocating. I'm not exaggerating when I say that it's *extremely* important
to have plenty of empty lines in your code. Using some empty lines to split this massive chunk of text into smaller pieces will make it much
easier to digest. Good places to insert empty lines are after loops and ``if`` statements.

That's the most obvious issue, but there's more. If you take a closer look at the code, you'll notice how inconsistent its formatting is:

* Sometimes there are spaces around operators (like in ``c2 == 'Rock'``), sometimes there aren't (``c2=='Paper'``), and sometimes there's one (``c1 =='Scissors'``).
* Sometimes there's a space after function names (``print ('Player 2 wins!')``) and other times there's not (``Outcome()``).
* Sometimes indents are 4 spaces wide and other times they're only 2.

In addition to that, there's a problem with some of the function and variable names. According to :pep:`8`, python's official style guide, variable names should follow this pattern:

* Classes should be named in ``CamelCase``.
* Functions and regular variables should be named in ``snake_case``.
* Constants (i.e. variables that should never be reassigned) should be named in ``UPPERCASE``.

If you follow these naming conventions, even someone who knows nothing about your code can instantly tell if a name is referring to a class, a function, a regular variable or a constant. (Even though functions and variables use the same naming scheme, it's easy to tell them apart because functions are usually followed by parentheses.)

Unfortunately, our code doesn't follow these conventions: The ``Outcome`` function is named in ``CamelCase`` like a class, as is the ``Game`` variable.

Let's fix all of that by applying official PEP 8 styling::

    def outcome():
        # check all combinations
        if c1 == c2:
            print('Tie!')
        elif ((c2 == 'Rock' and c1 == 'Paper') or
              (c2 == 'Paper' and c1 == 'Scissors') or
              (c2 == 'Scissors' and c1 == 'Rock')):
            print('Player 1 wins!')
        elif ((c1 == 'Rock' and c2 == 'Paper') or
              (c1 == 'Paper' and c2 == 'Scissors') or
              (c1 == 'Scissors' and c2 == 'Rock')):
            print('Player 2 wins!')


    while True:
        n = 0
        while n < 3:
            while True:
                # ask for user input
                c1 = input("Player 1: Rock, Paper, or Scissors? ")
                if c1 == 'Rock' or c1 == 'Paper' or c1 == 'Scissors':
                    break  # check passed

                print("Invalid input")

            while True:
                c2 = input("Player 2: Rock, Paper, or Scissors? ")
                if c2 == 'Rock' or c2 == 'Paper' or c2 == 'Scissors':
                    break

                print("Invalid input")

            n += 1  # increment counter by 1
            outcome()  # call outcome function

        game = input("Would you like to play again? ")
        if game == 'n' or game == 'N' or game == 'no' or game == 'No':
            break

An easy but worthwhile improvement.

Improvement #2: More expressive variable names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not a single variable in this code is named well. Let's look at a few:

* ``n``: "n" for "number". Great name, right? No, terrible name. This variable is used to count how many rounds were played so the game can stop after 3 rounds. So a better name for it would be ``round_num`` or something similar.
* ``c1`` and ``c2``: *Obviously* these are short for "choice 1" and "choice 2" and store each of the 2 players' inputs. Except it's not obvious at all. Let's rename these to ``player1_hand`` and ``player2_hand``.
* ``outcome``: This function prints the outcome of the game, so it's named ``outcome``. That's not a bad thought process, but the name is not good enough. It doesn't tell the reader that the function *prints* the outcome, so many people will assume that it *returns* the outcome. Let's be extra clear and rename this function to ``print_winner``.
* ``game``: If you see a variable with the name ``game``, what do you think its value could be? A number? A string? If it's hard to imagine what that variable's purpose could be, that's a sign of a bad variable name. We'll change this to ``play_again``.

Our code now looks like this::

    def print_winner():
        # check all combinations
        if player1_hand == player2_hand:
            print('Tie!')
        elif ((player2_hand == 'Rock' and player1_hand == 'Paper') or
              (player2_hand == 'Paper' and player1_hand == 'Scissors') or
              (player2_hand == 'Scissors' and player1_hand == 'Rock')):
            print('Player 1 wins!')
        elif ((player1_hand == 'Rock' and player2_hand == 'Paper') or
              (player1_hand == 'Paper' and player2_hand == 'Scissors') or
              (player1_hand == 'Scissors' and player2_hand == 'Rock')):
            print('Player 2 wins!')


    while True:
        round_num = 0
        while round_num < 3:
            while True:
                # ask for user input
                player1_hand = input("Player 1: Rock, Paper, or Scissors? ")
                if (player1_hand == 'Rock' or
                    player1_hand == 'Paper' or
                    player1_hand == 'Scissors'):
                    break  # check passed

                print("Invalid input")

            while True:
                player2_hand = input("Player 2: Rock, Paper, or Scissors? ")
                if (player2_hand == 'Rock' or
                    player2_hand == 'Paper' or
                    player2_hand == 'Scissors'):
                    break

                print("Invalid input")

            round_num += 1  # increment round counter by 1
            print_winner()  # call print_winner function

        play_again = input("Would you like to play again? ")
        if (play_again == 'n' or play_again == 'N' or
            play_again == 'no' or play_again == 'No'):
            break

Slowly but surely our code is improving.

Improvement #3: Eliminate duplicate code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you take a look at the code that asks both players to input Rock, Paper, or Scissors, you'll notice that it contains two very similar ``while True:`` loops. The only difference between the two loops is the name of the player ("Player 1" vs "Player 2") and the variable where they store the user input (``player1_hand`` vs ``player2_hand``).

Writing the same (or very similar) code more than once is almost never a good idea. If you ever have to make changes to this code, you have to make the same change twice. It makes your code harder to read, too. People might assume that there's a significant difference between the two loops, because why would you write two loops that do the same thing? They'll expect the 2nd loop to be different and try to find that difference, only to realize that both loops are actually equivalent. Your code creates certain expectations in the person reading it, and the more often those expectations turn out to be wrong, the more effort it takes for that person to understand your code.

So let's do everyone a favor and get rid of the duplicated code. One of the best ways to eliminate duplicate code is to use functions. Instead of writing the code twice, we'll wrap it in a function and call the function twice.

This is our code now::

    def input_player_hand(player_name):
        while True:
            # ask for user input
            hand = input(player_name + ": Rock, Paper, or Scissors? ")
            if hand == 'Rock' or hand == 'Paper' or hand == 'Scissors':
                return hand  # check passed

            print("Invalid input")


    def print_winner():
        # check all combinations
        if player1_hand == player2_hand:
            print('Tie!')
        elif ((player2_hand == 'Rock' and player1_hand == 'Paper') or
              (player2_hand == 'Paper' and player1_hand == 'Scissors') or
              (player2_hand == 'Scissors' and player1_hand == 'Rock')):
            print('Player 1 wins!')
        elif ((player1_hand == 'Rock' and player2_hand == 'Paper') or
              (player1_hand == 'Paper' and player2_hand == 'Scissors') or
              (player1_hand == 'Scissors' and player2_hand == 'Rock')):
            print('Player 2 wins!')


    while True:
        round_num = 0
        while round_num < 3:
            player1_hand = input_player_hand('Player 1')
            player2_hand = input_player_hand('Player 2')

            round_num += 1  # increment round counter by 1
            print_winner()  # call print_winner function

        play_again = input("Would you like to play again? ")
        if (play_again == 'n' or play_again == 'N' or
            play_again == 'no' or play_again == 'No'):
            break

Look at that difference! The code is so much shorter and cleaner!

Improvement #4: Replace global variables with function parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlike the ``print_winner`` function, the ``input_player_hand`` we just added accepts a parameter. Why is that? Is it because ``print_winner`` doesn't need input? That can't be it, because ``print_winner`` needs ``player1_hand`` and ``player2_hand`` as input. Maybe it uses global variables because those two variables already exist, whereas there is no global ``player_name`` variable that ``input_player_name`` could use. That makes sense, right?

Well, it does make sense, but using global variables as input for a function is still a bad idea. The problem with using global variables in a function is that it's hard to see which global variables the function depends on. If someone wants to find out how to pass input to the ``print_winner`` function, they have to read the whole function and look for global variables. That's the only way to find out that it accepts input through ``player1_hand`` and ``player2_hand``. Compared to that, figuring out how to pass input to the ``input_player_hand`` function is trivial - you can immediately see that it needs a ``player_name`` argument.

Readable code is code that clearly communicates its purpose to the reader. Function parameters do that. Global variables don't. So let's get rid of them.

::

    def input_player_hand(player_name):
        while True:
            # ask for user input
            hand = input(player_name + ": Rock, Paper, or Scissors? ")
            if hand == 'Rock' or hand == 'Paper' or hand == 'Scissors':
                return hand  # check passed

            print("Invalid input")


    def print_winner(player1_hand, player2_hand):
        # check all combinations
        if player1_hand == player2_hand:
            print('Tie!')
        elif ((player2_hand == 'Rock' and player1_hand == 'Paper') or
              (player2_hand == 'Paper' and player1_hand == 'Scissors') or
              (player2_hand == 'Scissors' and player1_hand == 'Rock')):
            print('Player 1 wins!')
        elif ((player1_hand == 'Rock' and player2_hand == 'Paper') or
              (player1_hand == 'Paper' and player2_hand == 'Scissors') or
              (player1_hand == 'Scissors' and player2_hand == 'Rock')):
            print('Player 2 wins!')


    while True:
        round_num = 0
        while round_num < 3:
            player1_hand = input_player_hand('Player 1')
            player2_hand = input_player_hand('Player 2')

            round_num += 1  # increment round counter by 1
            # call print_winner function
            print_winner(player1_hand, player2_hand)

        play_again = input("Would you like to play again? ")
        if (play_again == 'n' or play_again == 'N' or
            play_again == 'no' or play_again == 'No'):
            break

A tiny, yet huge improvement. Global variables often lead to spagetthi code, especially in larger programs.

Improvement #5: Use more functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As it turns out, functions have lots of good qualities:

1. The code in a function can be easily reused by calling the function.
2. Functions have names, which help us humans understand what the code in the function does.
3. Short code is easier to understand than long code, so splitting the program into shorter functions makes it easier to comprehend.

This 3rd point is a very important one. Humans have short attention spans. Reading 50 lines of code and remembering all the stuff that happens - for example, keeping track of all the variables and their values - is *hard*. Reading 5 blocks with 10 lines each tends to be much easier, as long as each of those 5 blocks has a clear purpose. And a short block with a clear purpose is exactly what a function should be.

So how can we split our program into functions that are short and easy to understand? Well, let's think about the flow of our game. In order, this is everything that happens:

1. Each player chooses a hand.
2. The winner of the round is displayed.
3. Everything that happened so far is repeated 3 times.
4. Once 3 rounds have been played, the user may restart the game.

We already have a function that asks a player to choose a hand. We also have a function that displays the winner of a round. What other functions could we create? Here are some ideas:

1. A function that plays one round of the game. (Ask each player for input and display the winner.)
2. A function that plays three rounds.
3. A function that asks the player if they want to restart.

Sounds like a plan. Here we go::

    def input_player_hand(player_name):
        while True:
            # ask for user input
            hand = input(player_name + ": Rock, Paper, or Scissors? ")
            if hand == 'Rock' or hand == 'Paper' or hand == 'Scissors':
                return hand  # check passed

            print("Invalid input")


    def print_winner(player1_hand, player2_hand):
        # check all combinations
        if player1_hand == player2_hand:
            print('Tie!')
        elif ((player2_hand == 'Rock' and player1_hand == 'Paper') or
              (player2_hand == 'Paper' and player1_hand == 'Scissors') or
              (player2_hand == 'Scissors' and player1_hand == 'Rock')):
            print('Player 1 wins!')
        elif ((player1_hand == 'Rock' and player2_hand == 'Paper') or
              (player1_hand == 'Paper' and player2_hand == 'Scissors') or
              (player1_hand == 'Scissors' and player2_hand == 'Rock')):
            print('Player 2 wins!')


    def play_round():
        player1_hand = input_player_hand('Player 1')
        player2_hand = input_player_hand('Player 2')
        
        # call print_winner function
        print_winner(player1_hand, player2_hand)


    def play_game():
        round_num = 0
        while round_num < 3:
            play_round()

            round_num += 1


    def play_games_forever():
        while True:
            play_game()

            play_again = input("Would you like to play again? ")
            if (play_again == 'n' or play_again == 'N' or
                play_again == 'no' or play_again == 'No'):
                break


    play_games_forever()

That's a lot more organized than before. The code we started with was a mess with a whopping 5 levels of indentation, but now we're down to 3. It's as `the Zen of Python <https://www.python.org/dev/peps/pep-0020/>`_ says: Flat is better than nested.

Improvement #6: Write useful comments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's take a look at the comments in the code and think about whether they add any useful information.

1. ::

      # ask for user input
      hand = input(player_name + ": Rock, Paper, or Scissors? ")
      
   Considering that there's an ``input()`` call in the very next line, this comment seems rather pointless. We can see that the code is asking for user input here, we don't need a comment to tell us that.

2. ::

      def print_winner(player1_hand, player2_hand):
          # check all combinations
          
   Well yeah, determining the winner is done by comparing the two players' hands. This comment hardly conveys any new information.
3. ::
        
      # call print_winner function
      print_winner(player1_hand, player2_hand)
    
   This one's even more useless than the others. We can *see* that function call, thank you very much.

None of these comments make the code easier to understand. They only state the obvious. Good comments should do (at least) one of four things:

1. Explain **how** the code is doing something, for example::

      # The stylesheets for the theme switcher are created in 3 steps:
      # 1. The available themes are loaded.
      # 2. The default theme is determined and removed from the list.
      # 3. The remaining themes are converted to CSS files.
2. Explain **why** the code is doing something, for example::

      # Because the create_theme_switcher_js function needs to read a
      # config value, we have to wait until the config has been processed
      # before we can call it.
      app.connect('config-parsed', create_theme_switcher_js)
3. Give background information about something, for example to inform other programmers that a specific edge case has been accounted for and will work correctly::

      # Register our javascript file.
      # Even though this file will only be created later, the build system
      # doesn't care - it'll happily insert a link to the script even
      # if the file doesn't exist (yet).
      app.add_js_file(theme_switcher_js)
4. Explain **what** a piece of code is doing. These are probably the worst kinds of comments - code should be self-explanatory if possible. Example::

      # This looks up a style by its id, then converts it to CSS
      style = sphinx.highlighting.PygmentsBridge.get_style(None, style_id)
      return pygments.HtmlFormatter(style=style).get_style_defs()

Our Rock-Paper-Scissors code is actually so simple that it doesn't need any comments at all. So instead of writing comments, we're going to add `docstrings <https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring>`_ to all our functions. Docstrings are pretty similar to comments: They explain what the code is doing in a way that's easy for humans to understand.

::

    def input_player_hand(player_name):
        """
        Asks the player to input "Rock", "Paper", or "Scissors".
        This is repeated until valid input is received.
        Returns a string containing the user's input, capitalized.
        """
        
        while True:
            hand = input(player_name + ": Rock, Paper, or Scissors? ")
            if hand == 'Rock' or hand == 'Paper' or hand == 'Scissors':
                return hand

            print("Invalid input")


    def print_winner(player1_hand, player2_hand):
        """
        Takes two player hands as input and prints the winner (or "Tie").
        """
        
        if player1_hand == player2_hand:
            print('Tie!')
        elif ((player2_hand == 'Rock' and player1_hand == 'Paper') or
              (player2_hand == 'Paper' and player1_hand == 'Scissors') or
              (player2_hand == 'Scissors' and player1_hand == 'Rock')):
            print('Player 1 wins!')
        elif ((player1_hand == 'Rock' and player2_hand == 'Paper') or
              (player1_hand == 'Paper' and player2_hand == 'Scissors') or
              (player1_hand == 'Scissors' and player2_hand == 'Rock')):
            print('Player 2 wins!')


    def play_round():
        """
        Plays a single round of Rock-Paper-Scissors.
        Asks both players for input and prints the outcome of the round.
        """
    
        player1_hand = input_player_hand('Player 1')
        player2_hand = input_player_hand('Player 2')

        print_winner(player1_hand, player2_hand)


    def play_game():
        """
        Plays 3 rounds of Rock-Paper-Scissors.
        """
    
        round_num = 0
        while round_num < 3:
            play_round()

            round_num += 1


    def play_games_forever():
        """
        Plays 3 rounds of Rock-Paper-Scissors, then asks the user if
        they want to play again.
        """
        
        while True:
            play_game()

            play_again = input("Would you like to play again? ")
            if (play_again == 'n' or play_again == 'N' or
                play_again == 'no' or play_again == 'No'):
                break


    play_games_forever()


Improvement #7: Finishing touches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At this point we're pretty much done. All that's left are some minor improvements. Remember, readable code has to clearly communicate its purpose to the reader. This often works best if you're concise; being too wordy can be detrimental. There are still a few places in the code where we could communicate our intentions more clearly.

1. **Don't write** ``elif`` **when you mean** ``else``: In the ``print_winner`` function, there are 3 possible outcomes: A tie, player 1 wins, or player 2 wins. So if it's not a tie and player 1 didn't win, then the winner must be player 2. And yet, our code goes to the trouble of comparing both players' hands before it prints "Player 2 wins!" instead of just using an ``else:``.
2. **Be concise**: Like I said before, good code should avoid being too lengthy. Don't misunderstand, though: I'm not saying that you should make your code as short as possible. The goal is to end up with simple code, not to overwhelm the reader with information because the code is doing too many things at the same time. Many people end up overdoing it and compress code like this::
  
       max_len = max(len(list1), len(list2))
       padded_list1 = list1 + [1] * (max_len - len(list1))
       padded_list2 = list2 + [1] * (max_len - len(list2))
       result = [x * y for x, y in zip(padded_list1, padded_list2)]
  
   into horrible one-liners like this::
  
       result = [x * y for x, y in zip(list1 + [1] * (len(list2) - len(list1)), list2 + [1] * (len(list1) - len(list2)))]

   That's concise, sure, but it's also awfully hard to read. Making code shorter is only a good idea if the code remains simple.
   
   Fortunately for us, there are some simple ways to shorten our code:

   * All the ``play_game`` function does is to call another function 3 times. It's only 4 lines of code, but 3 of those lines are used for looping and counting to 3. We can do better than that - replacing the ``while`` loop with a ``for round_num in range(3):`` saves 2 lines of code. But then there's another improvement to make: Since the ``round_num`` variable is never used for anything, it's best to rename it to ``_`` (underscore), a name conventionally used for throwaway variables.
   * In ``play_games_forever`` we compare the ``play_again`` variable to 4 different strings. 2 of those strings are actually the same except with different capitalization. So we can shorten this code just by normalizing the case of the user input.
   * We always used a bunch of ``or`` clauses to compare a variable against multiple different values (e.g. in ``input_player_hand`` or ``play_games_forever``), but the same thing could be achieved by storing all valid values in a container like a list or a set and performing a membership test on that container. For example, instead of writing ``x == 1 or x == 2``, you can write ``x in {1, 2}``.

After making these last few changes, our code looks like this::

    def input_player_hand(player_name):
        """
        Asks the player to input "Rock", "Paper", or "Scissors".
        This is repeated until valid input is received.
        Returns a string containing the user's input, capitalized.
        """
        
        while True:
            hand = input(player_name + ": Rock, Paper, or Scissors? ")
            if hand in {'Rock', 'Paper', 'Scissors'}:
                return hand

            print("Invalid input")


    def print_winner(player1_hand, player2_hand):
        """
        Takes two player hands as input and prints the winner (or "Tie").
        """
        
        if player1_hand == player2_hand:
            print('Tie!')
        elif (player2_hand, player1_hand) in {('Rock', 'Paper'),
                                              ('Paper', 'Scissors'),
                                              ('Scissors', 'Rock')}:
            print('Player 1 wins!')
        else:
            print('Player 2 wins!')


    def play_round():
        """
        Plays a single round of Rock-Paper-Scissors.
        Asks both players for input and prints the outcome of the round.
        """
    
        player1_hand = input_player_hand('Player 1')
        player2_hand = input_player_hand('Player 2')

        print_winner(player1_hand, player2_hand)


    def play_game():
        """
        Plays 3 rounds of Rock-Paper-Scissors.
        """
    
        for _ in range(3):
            play_round()


    def play_games_forever():
        """
        Plays 3 rounds of Rock-Paper-Scissors, then asks the user if
        they want to play again.
        """
        
        while True:
            play_game()

            play_again = input("Would you like to play again? ")
            if play_again.lower() in {'n', 'no'}:
                break


    play_games_forever()

And just like that, we transformed messy spagetthi code into beautiful python.

Unfortunately I couldn't cram everything I wanted to address into this small Rock-Paper-Scissors game, so here's one more tip:

Improvement #8: Name your values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've already used functions to give chunks of code a name, but values are another thing that benefits from having a name. This is mostly relevant when you're working with data structures, like lists or dicts. Instead of repeatedly accessing an element by its index or key like this::

    def find_book_by_isbn(isbn):
        for book_id in books_by_id_dict:
            if books_by_id_dict[book_id]['ISBN'] == isbn:
                return books_by_id_dict[book_id]

You should assign it to a variable like this::

    def find_book_by_isbn(isbn):
        for book_id in books_by_id_dict:
            book = books_by_id_dict[book_id]
            
            if book['ISBN'] == isbn:
                return book

Conclusion
==========

There are many ways to improve the readability of your code. Individually, each is only a minor improvement - but they add up quickly. Keeping your code readable while you're trying to be productive and write code that just gets the job done is probably going to be difficult at first. You're going to get sloppy. That's normal, it happens to everyone. As always, the key to mastering writing readable code is practice. A lot of it. In fact, writing readable code is so difficult that not a single person will *ever* master it. Just keep going at it, and you'll never stop getting better at it.
