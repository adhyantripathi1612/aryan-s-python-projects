def email_slicer(email):
    if email.count('@') == 1:
        username, domain = email.split('@')
        valid_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com', 
            'aol.com', 'msn.com', 
            'yahoo.co.in', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.fr', 'yahoo.de', 
            'yahoo.co.jp', 'yahoo.es', 'yahoo.it', 
            'hotmail.co.uk', 'hotmail.fr', 'hotmail.de', 'hotmail.it', 'hotmail.es',
            'comcast.net', 'verizon.net', 'att.net', 'sbcglobal.net', 'charter.net',
            'rediffmail.com', 'indiatimes.com', 'rediff.com', 'in.com', 'juno.com',
            'orange.fr', 'wanadoo.fr', 'free.fr', 'laposte.net', 'voila.fr',
            'gmx.net', 'gmx.de', 'web.de', 't-online.de', 'freenet.de',
            'yandex.ru', 'mail.ru', 'rambler.ru', 'list.ru', 'bk.ru',
            'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
            'icloud.com', 'me.com', 'mac.com', 'protonmail.com', 'zoho.com',
            'fastmail.com', 'mail.com', 'yahoo.ca', 'rogers.com', 'shaw.ca'
        }
        
        if domain in valid_domains:
            print(f"Username: {username}")
            print(f"Domain:   {domain}")
        else:
            print("Invalid domain: Not in approved providers list.")
            print("(Try: gmail.com, yahoo.com, hotmail.com, etc.)")
    else:
        print("Invalid email: Must contain exactly one '@'.")

print("--- Email Slicer (50+ Domains) ---")
print("Type 'exit' or 'done' to quit.\n")

while True:
    user_input = input('Enter the email to slice: ').strip().lower()

    if user_input in ['exit', 'done', 'quit']:
        print("Goodbye!")
        break
    
    if not user_input:
        continue

    email_slicer(user_input)
    print()