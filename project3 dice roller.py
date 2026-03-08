import random

def dice_rolling():
     while True:
        print('This is Adhyan Tripathi\'s dice roller ')
        print('If you want to roll the dice, type "roll"')
        print('if you want to exit, type "exit"')

        choice = input('enter the choice here -: ')

        if choice == 'roll':
            roll = random.randint(1, 6)
            print(f'you rolled a {roll}')

        elif choice != 'roll' and choice != 'exit':
            print('invalid choice, please try again')
        
        elif choice == 'exit':
            print('goodbye!')
            break
        
            
if __name__ == '__main__':
    dice_rolling()




