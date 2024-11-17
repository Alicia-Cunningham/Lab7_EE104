from pynq import GPIO
from time import sleep

delay = 0.5
current_position = 1

f1  =        GPIO(GPIO.get_gpio_pin(0), 'out')
f2  =        GPIO(GPIO.get_gpio_pin(1), 'out')
f3  =        GPIO(GPIO.get_gpio_pin(2), 'out')
f4  =        GPIO(GPIO.get_gpio_pin(3), 'out')
sos_led =    GPIO(GPIO.get_gpio_pin(7), 'out')

floors = [f1, f2, f3, f4]

def start():
    global current_position
    current_position = 1
    f1.write(1)
    f2.write(0)
    f3.write(0)
    f4.write(0)
    sos_led.write(0)

def move(desired_position, ada):
    global current_position
    ada_delay = 0
    distance = abs(desired_position - current_position)
    result = "You are now on floor {}"
    
    if ada:
        ada_delay = 0.5
        print("We will get you to your destination safely!")
    
    if desired_position > current_position: #Moving Up
        open(floors[current_position - 1])
        for i in range(distance):
            floors[current_position - 1].write(0)
            sleep(delay + ada_delay)
            current_position += 1
            floors[current_position - 1].write(1)
        print(result.format(current_position))
    elif desired_position < current_position: #Moving Down
        open(floors[current_position - 1])
        for i in range(distance):
            floors[current_position - 1].write(0)
            sleep(delay + ada_delay)
            current_position -= 1
            floors[current_position - 1].write(1)
        print(result.format(current_position))
    elif desired_position == current_position: #Do Nothing
        print("You are already on this floor.")

def open(led): #Blink the light
    for i in range(10):
        led.write(1)
        sleep(delay)
        led.write(0)
        sleep(delay)

def ada():
    floor = input("Enter your desired floor number: ")
    move(int(floor), True)

def sos():
    start()
    open(sos_led)
    print("You are on floor 1, help is on the way!")

def elevator():
    start()
    while True:
        
        action = input("Welcome to the Elevator: ").lower()
        
        if action in {"1", "2", "3", "4"}:
            move(int(action), False)
        elif action == "ada":
            ada()
        elif action == "sos":
            sos()
        elif action == "quit":
            return
        else:
            print("Please enter a floor from 1 to 4.\nIf you have a disability please enter 'ada'\nFor emergencies enter 'sos'")
        
        

elevator()