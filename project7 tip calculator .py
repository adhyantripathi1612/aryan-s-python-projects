def tip_calculator(): 
    payer = float(input('Enter the total amount here: '))
    
    tip_input = input('Enter the percentage (10, 15, 20) or "no": ')
    
    
    if tip_input == "no":
        print(f"Total bill: {payer:.2f}")
        return 
    
    
    tip = int(tip_input)
    
    bill_after_tip = payer * (tip / 100)
    total_bill = bill_after_tip + payer
  
    print(f"Your total bill is: {total_bill:.2f}")

tip_calculator()
