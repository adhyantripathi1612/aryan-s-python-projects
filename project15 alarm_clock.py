import time
import winsound

H = int(input('Enter the hour at which you want to set the alarm (1-12): '))
M = int(input('Enter the minute at which you want to set the alarm (0-59): '))
AM_PM = input('AM or PM?: ').strip().upper()

# Format with zero-padding to match strftime '%I:%M %p' e.g. "07:05 PM"
alarm_time = f'{H:02}:{M:02} {AM_PM}'

print(f'Alarm is set for {alarm_time}')
print('Waiting for alarm...\n')

def alarm():
    for i in range(86400):  # loop for up to 24 hours (86400 seconds)
        # %I is 12-hour format, %M is minutes, %p is AM/PM
        current_time = time.strftime('%I:%M %p')

        if current_time == alarm_time:
            print(f'ALARM RINGING! Time is {current_time}')
            # Beep sound: frequency=1000Hz, duration=1000ms (repeat 5 times)
            for i in range(5):
                winsound.Beep(1000, 1000)
            break
        else:
            print(f'Current time: {current_time} | Alarm set for: {alarm_time}')
            time.sleep(60)  # check every 60 seconds

alarm()
