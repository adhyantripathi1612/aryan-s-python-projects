def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi


def main():
    while True:
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height in meters: "))
        bmi = calculate_bmi(weight, height)
        print(f"Your BMI is: {bmi:.2f}")
        
        # BMI Level Classification
        if bmi < 18.5:
            print("Your BMI is LOW (Underweight)")
        elif bmi < 25:
            print("Your BMI is NORMAL (Healthy weight)")
        elif bmi < 30:
            print("Your BMI is HIGH (Overweight)")
        else:
            print("Your BMI is VERY HIGH (Obese)")
        
        # Ask if user wants to continue
        user_input = input("\nDo you want to calculate another BMI? (type 'exit' to stop): ").lower()
        if user_input == "exit":
            print("Thank you for using the BMI Calculator! Goodbye!")
            break
        print()



if __name__ == "__main__":
    main()