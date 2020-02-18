
######################
Writing efficient code
######################


1) Readability (meaningful variable names, comments, no huge walls of code, ...)
2) Efficiency (runtime/space complexity)
3) Maintainability (proper use of functions/OOP, no global variables, single responsibility principle, ...)
4) Documentation, testing


1) nondescript variable/class/function names
2) lots of duplicated code
3) error handling by returning None/False/an error string
4) no separation between game logic and user interface
5) useless comments
6) hard-coding values
7) global variables/instance attributes instead of function parameters
8) using the same variable for objects of different kinds
9) useless classes (with no state)
10) side effects (os.chdir, ...)


::

    import random

    # class built only to be inherited by other classes
    class Shared_Attributes:
        def __init__(self):
            self.health = 100
            self.power = 100
            self.power_type = 'Mana'
            self.health_potion = 3
            self.power_potion = 3

        def use_health_potion(self):
            if self.health_potion > 0:
                self.health_potion -= 1
                self.health += 25
                return f'Health Potion healed 25 hitpoints, you now have {self.health} hitpoints left.'
            else:
                return 'You have no Health Potions left.'

        def use_power_potion(self):
            if self.power_potion > 0:
                self.power_potion -= 1
                self.power += 25
                return f'{self.power_type} Potion restored 25 {self.power_type.lower()}, you now have {self.power} {self.power_type.lower()} left.'
            else:
                return f'You have no {self.power_type} Potions left.'


    class Mage(Shared_Attributes):
        def throw_fireball(self, enemy):
            dmg = random.randint(20, 30)
            enemy.health -= dmg
            print(f'You deal {dmg} damage.')

        def lesser_heal(self):
            heal = random.randint(20, 30)
            self.health += heal
            print(f'You gain {heal} health.')

        def skill_menu(self):
            pass


    class Knight(Shared_Attributes):
        def __init__(self):
            super().__init__()
            self.power_type = 'Stamina'

        def heroic_strike(self):
            dmg = random.randint(25, 30)
            enemy.health -= dmg
            print(f'You deal {dmg} damage.')

        def first_aid(self):
            heal = random.randint(15, 20)
            self.health += heal
            print(f'You gain {heal} health.')


    def check_for_win():
        if player_one.health <= 0:
            print('Player Two wins!')
            return True
        elif player_two.health <=0:
            print('Player One wins!')
            return True
        else:
            return False


    def assign_character(player_choice):
        if player_choice == 'Knight':
            return Knight()
        elif player_choice == 'Mage':
            return Mage()
        else:
            return 'Invalid'


    if __name__ == '__main__':
        game_state = input('Are you ready to play? (y or n): ').lower()

        while game_state == 'y':
            print('Character Choices: Knight, Mage')
            player_one = assign_character(input('Player One, choose your character: '))
            player_two = assign_character(input('Player Two, choose your character: '))

            while not check_for_win():
                player_one.skill_menu()
                if check_for_win():
                    break

                player_two.skill_menu()

            game_state = input('Do you want to play again? (y or n): ').lower()
