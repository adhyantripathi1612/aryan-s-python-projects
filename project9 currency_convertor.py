def convert_currency():
    amount = float(input("Enter the amount to convert: "))
    from_currency = input("Enter the source currency (USD, EUR, INR, GBP, JPY, AUD): ").strip().upper()
    to_currency = input("Enter the target currency (USD, EUR, INR, GBP, JPY, AUD): ").strip().upper()

    if from_currency == "USD" and to_currency == "EUR":
        converted_amount = amount * 0.85

    elif from_currency == "EUR" and to_currency == "USD":
        converted_amount = amount * 1.18

    elif from_currency == "INR" and to_currency == "GBP":
        converted_amount = amount * 0.012

    elif from_currency == "GBP" and to_currency == "INR":
        converted_amount = amount * 83.33

    elif from_currency == "JPY" and to_currency == "AUD":
        converted_amount = amount * 0.012

    elif from_currency == "AUD" and to_currency == "JPY":
        converted_amount = amount * 83.33

    elif from_currency == "INR" and to_currency == "USD":
        converted_amount = amount * 0.012

    elif from_currency == "USD" and to_currency == "INR":
        converted_amount = amount * 83.33

    else:
        print("Currency conversion not supported. Instead, please choose from the following options:")
        print("1. USD to EUR")
        print("2. EUR to USD")
        print("3. INR to GBP")
        print("4. GBP to INR")
        print("5. JPY to AUD")
        print("6. AUD to JPY")
        return
    
    print(f"{amount} {from_currency} = {converted_amount} {to_currency}")

convert_currency()
        


# project9 done 7/3/2026