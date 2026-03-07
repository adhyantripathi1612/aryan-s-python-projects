import time

print('this is a digital clock by Adhyan Tripathi, if you want to exit the clock, just press ctrl + c')

def digital_clock():

    while True:
        current_time = time.strftime("%H:%M:%S")
        print('the current time running is -:' + current_time, end="\r")
        time.sleep(1)



if __name__ == "__main__":
    digital_clock()