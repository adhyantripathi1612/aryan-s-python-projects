print('this is a timer')

import time

a = int(input('enter the number of seconds for the timer to run-: '))

print('timer started')

for i in range(a):
    print(f'{a-i} seconds left')
    time.sleep(1)

print('timer ended')

# fourth project done 3/3/2026