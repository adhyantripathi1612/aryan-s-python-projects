def calculator():
    
    while True:
        c = input("Enter the operation (+, -, *, /,%) or 'q' to quit: ")
        
        if c == 'q':
            print("Goodbye!")
            break
        elif c == 'Q':
            print('if you want to quit, please enter "q" not "Q".')
            continue
        
        elif c != "+" and c != "-" and c != "*" and c != "/" and c != "%":
            print("Invalid operation. Please choose +, -, *, /, % or 'q'.")
            continue    
        
        try:
            a = float(input("Enter the first number: "))
            b = float(input("Enter the second number: "))
        
        except ValueError:
            print("Invalid input; please enter numeric values.")
            continue

        
        if c == "+":
            result = a + b
            print('the result is-: ', result)

  
        elif c == "-":
            result = a - b
            print('the result is-: ', result)

  
        elif c == "*":
            result = a * b
            print('the result is-: ', result)

  
        elif c == "/":
            if b != 0:
                result = a / b
                print('the result is-: ', result)
  
            else:
                print("Error: Division by zero is not allowed.")

        elif c == "%":
            if b != 0:
                result = a % b
                print('the result is-: ', result)
  
            else:
                print("Error: Division by zero is not allowed.")


  
        else:
            print("Unknown operation. Please choose +, -, *, / or 'q'.")


if __name__ == "__main__":
    calculator()
    



# first project completed successfully YIPPEE! 28/2/2026