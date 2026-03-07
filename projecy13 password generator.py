import random
import string
import time 

first_password = ""  # Store first password globally

while True:
    user_input = input("enter the length of the password or exit to quit: ")
    
    if user_input.lower() == "exit":
        break
        
    try:
        user = int(user_input)
    except:
        print("Please enter a valid number!")
        continue

    def for_letters():
        global first_password
        u1 = input("do you want to include letters? (y/n): ")
        if u1.lower() == "y":
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=user))
            first_password = password  # Save first password
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)
        else:
            password = ''.join(random.choices(string.digits + string.punctuation, k=user))
            first_password = password  # Save first password
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)

    def for_digits():
        u2 = input("do you want to include digits? (y/n): ")
        if u2.lower() == "y":
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=user))
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)
        else:
            password = ''.join(random.choices(string.ascii_letters + string.punctuation, k=user))
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)

    def for_punctuation():
        u3 = input("do you want to include punctuation? (y/n): ")
        if u3.lower() == "y":
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=user))
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)
        else:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=user))
            time.sleep(2)
            print("generating password...")
            print('password generated -: ', password)

    def for_all():
        global first_password
        u1 = input("letters? (y/n): ")
        u2 = input("digits? (y/n): ")
        u3 = input("punctuation? (y/n): ")
        if u1.lower() == "y" and u2.lower() == "y" and u3.lower() == "y":
            new_part = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=user))
            password = first_password + new_part  # ADD first password to final
            time.sleep(2)
            print("generating password...")
            print('FINAL password generated -: ', password)
            print(f"Length: {len(password)} (first: {len(first_password)} + new: {len(new_part)})")

    if __name__ == "__main__":
        for_letters()
        for_digits()
        for_punctuation()
        for_all()
