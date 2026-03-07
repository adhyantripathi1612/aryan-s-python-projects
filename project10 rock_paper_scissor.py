import random
import time
while True:

    print('This is a Rock, Paper, Scissor game, by Adhyan Tripath!i')

    user = input('enter your choice (rock, paper, scissor): or type "quit" to exit the game -: ').lower()
    
    time.sleep(0.5)
    
    computer = random.choice(['rock', 'paper', 'scissor'])

    def rock():
  
        if user == 'rock' and computer == 'scissor':
            
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')
            
            time.sleep(0.5)

            print('You win!')

        elif user == 'rock' and computer == 'paper':
            
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')
            
            time.sleep(0.5)

            print('You lose!')

        else:
            
            time.sleep(0.5)

            print('It is a tie!')

    def paper():
    
        if user == 'paper' and computer == 'rock':
            
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')
            
            time.sleep(0.5)

            print('You win!')

        elif user == 'paper' and computer == 'scissor':
            
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')
            
            time.sleep(0.5)

            print('You lose!')

        else:
            
            time.sleep(0.5)

            print('It is a tie!')

    def scissor():

        if user == 'scissor' and computer == 'paper':
            
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')
            
            time.sleep(0.5)

            print('You win!')

        elif user == 'scissor' and computer == 'rock':
           
            time.sleep(0.5)
            
            print(f'Computer chose {computer}.')

            time.sleep(0.5)

            print('You lose!')

        else:
            
            time.sleep(0.5)
            
            print('It is a tie!')


    def quit():
        
        if user == 'quit':
            
            time.sleep(0.5)
            
            print('Thanks for playing! Goodbye!')
            exit()
             


    if __name__ == "__main__":
       
        if user == 'rock':
            rock()

       
        elif user == 'paper':
            paper()

       
        elif user == 'scissor':
            scissor()

       
        elif user == 'quit':
            print('Thanks for playing! Goodbye!')
            break 




# projexct10 done 7/3/2026

        