<<<<<<< HEAD
import random

def number_guessing_game():
    low = 1
    high = 100
    
    print("Think of a number between 1 and 100")
    
    while True:
        guess = (low + high) // 2
        print(f"Computer guesses: {guess}")
        
        response = input("Is it correct, too high, or too low? (correct/high/low): ").lower()
        
        if response == "correct":
            print("Computer guessed correctly!")
            break
        elif response == "high":
            high = guess - 1
        elif response == "low":
            low = guess + 1
        else:
            print("Please enter 'correct', 'high', or 'low'")


=======
import random

def number_guessing_game():
    low = 1
    high = 100
    
    print("Think of a number between 1 and 100")
    
    while True:
        guess = (low + high) // 2
        print(f"Computer guesses: {guess}")
        
        response = input("Is it correct, too high, or too low? (correct/high/low): ").lower()
        
        if response == "correct":
            print("Computer guessed correctly!")
            break
        elif response == "high":
            high = guess - 1
        elif response == "low":
            low = guess + 1
        else:
            print("Please enter 'correct', 'high', or 'low'")


>>>>>>> 3f7e543e3da3f338aae73938f5603f57c2c87d25
number_guessing_game()