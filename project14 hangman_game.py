import random

a = ['python', 'java', 'kotlin', 'javascript', 'hangman', 'programming', 'developer', 'computer', 'algorithm', 'function']

word = random.choice(a).lower()  

MAX_WRONG = 6

wrong_guesses = 0

guessed = []

print('Hangman Game by Adhyan Tripathi. Type "exit" to quit.')

def hangman():
    global wrong_guesses
    print(f'The word has {len(word)} letters')
    
    while wrong_guesses < MAX_WRONG:
        
        display = ''
        
        for letter in word:
        
            if letter in guessed:
        
                display += letter + ' '
        
            else:
        
                display += '_ '
        
        print(f'\n{display.strip()}')
        
        print(f'Wrong guesses left: {MAX_WRONG - wrong_guesses}')
        
        
        while True:
        
            guess = input('Guess a letter: ').lower().strip()
        
            if guess == 'exit':
        
                print('Thanks for playing!')
        
                return
        
            if len(guess) == 1 and guess.isalpha():
        
                break
        
            print('Enter a SINGLE LETTER only!')
        

        
        if guess in guessed:
        
            print('You already guessed that letter!')
        
            continue


        
        guessed.append(guess)
        

        
        if guess in word:
        
            print('Good guess!')
        else:
        
            print('Wrong guess!')
        
            wrong_guesses += 1
        

        
        display = ''.join([letter if letter in guessed else '_' for letter in word])
        
        if display == word:
        
            print(f'\n🎉 CONGRATULATIONS! You won! Word was: {word}')
        
            break
    

    
    if wrong_guesses == MAX_WRONG:
    
        print(f'\n💀 GAME OVER! Word was: {word}')


hangman()
