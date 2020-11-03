from intruder import Intruder
from intruder import Intruder
from aircraft import Aircraft
from statistics import mean, stdev
from numpy import arange
import math

# Channel Properties
while True:
    try:
        print("\nPlease key in the properties of the channel: \n")
        CHANNEL_X = int(input("Length of Channel: "))
        CHANNEL_Y = int(input("Width of Channel: "))
    except ValueError:
        print("\nPlease key in an integer\n")
        continue

    if CHANNEL_X <= 0 or CHANNEL_Y <= 0:
        print("\nLength and width of channel must be larger than 0\n")
        continue
    else:
        break

# Aircraft Properties
while True:
    try:
        print("\nPlease key in the properties of the aircraft: \n")
        AIRCRAFT_SPEED = int(input("Speed of aircraft: "))
        SENSOR_RANGE = int(input("Range of Sensor: "))

    except ValueError:
        print("\nPlease key in an integer\n")
        continue

    if AIRCRAFT_SPEED <= 0 or SENSOR_RANGE <= 0:
        print("\nAircraft speed and sensor range must be larger than 0\n")
        continue
    else:
        break
    
AIRCRAFT_STARTING_X = CHANNEL_X // 2
AIRCRAFT_STARTING_Y = 0

# Intruder properties
while True:
    try:
        print("\nPlease key in the properties of the intruder: \n")
        INTRUDER_SPEED = int(input("Speed of Intruder: "))


    except ValueError:
        print("\nPlease key in an integer or a float\n")
        continue

    if INTRUDER_SPEED <= 0:
        print("\nIntruder speed must be larger than 0\n")
        continue
    else:
        break

# Other properties
while True:
    try:
        print("\nPlease key in the properties for testing: \n")
        NUM_INTRUDERS = int(input("Number of intruders per sample: "))
        SAMPLE_SIZE = int(input("Sample size: "))
        DECIMAL_PLACES = int(input("Decimal of testing: "))


    except ValueError:
        print("\nNumber of intruders and sample size must be integers\n")
        continue

    if NUM_INTRUDERS <= 0 or SAMPLE_SIZE <= 0 or DECIMAL_PLACES <= 0:
        print("\n\nValues must be larger than 0\n")
        continue
    else:
        break


def main():
    opt_radius = optimal_radius()
    print(f"Optimal radius is {opt_radius[0]} and it caught {opt_radius[1]} intruders with a standard deviation of {opt_radius[2]}")

    opt_xspeed = optimal_zigzag()
    print(f"Optimal xspeed is {opt_xspeed[0]} and it caught {opt_xspeed[1]} intruders with a standard deviation of {opt_xspeed[2]}")

    rand_move = random_movement()
    print(f"Random movement catches {rand_move[0]} intruders with a standard deviation of {rand_move[1]}")


def single_sample(pathtype, x_speed=0, radius=0):

    number_intruders_caught = 0

    for _ in range(NUM_INTRUDERS):

        aircraft = Aircraft(speed=AIRCRAFT_SPEED,
                    x_pos=AIRCRAFT_STARTING_X,
                    y_pos=AIRCRAFT_STARTING_Y,
                    sensor_range=SENSOR_RANGE,
                    channel_x=CHANNEL_X,
                    channel_y=CHANNEL_Y)

        # Create instance of intruder
        intruder = Intruder(speed=INTRUDER_SPEED, 
                            channel_x=CHANNEL_X, 
                            channel_y=CHANNEL_Y)


        while intruder.x_pos < CHANNEL_X:

            if pathtype == "ZIGZAG":
                aircraft.move_zigzag(x_speed)

            elif pathtype == "CIRCULAR":
                aircraft.move_circular(radius)
            
            elif pathtype == "RANDOM":
                aircraft.move_random()

            intruder.move()

            if aircraft.check_intruder(intruder):
                number_intruders_caught += 1
                break
    
    return number_intruders_caught


def optimal_radius():

    max_radius = (CHANNEL_Y - AIRCRAFT_STARTING_Y) // 2

    max_intruders_caught = 0
    std = 0
    optimal_radius = 0

    for radius in range(1, max_radius):
        

        # Collect samples
        intr_caught = []

        for _ in range(SAMPLE_SIZE):

            intr_caught.append(single_sample("CIRCULAR", radius=radius))

        # Calculate mean catch rate of this radius
        mean_intr_caught = mean(intr_caught)

        # Store if greater than existing one
        if mean_intr_caught > max_intruders_caught:
            max_intruders_caught = mean_intr_caught
            std = round(stdev(intr_caught),DECIMAL_PLACES)
            optimal_radius = radius

    return (optimal_radius, max_intruders_caught, std)
    

def optimal_zigzag():

    max_intruders_caught = 0
    std = 0
    optimal_x_speed = 0

    for x_speed in range(-AIRCRAFT_SPEED, AIRCRAFT_SPEED+1):
        
        # Collect samples
        intr_caught = []

        for _ in range(SAMPLE_SIZE):

            intr_caught.append(single_sample("ZIGZAG", x_speed=x_speed))

        # Calculate mean catch rate of this x_speed
        mean_intr_caught = mean(intr_caught)

        # Store if greater than existing one
        if mean_intr_caught > max_intruders_caught:
            max_intruders_caught = mean_intr_caught
            std = round(stdev(intr_caught),DECIMAL_PLACES)
            optimal_x_speed = x_speed

    return (optimal_x_speed, max_intruders_caught, std)


def random_movement():

    # Collect samples
    intr_caught = []

    for _ in range(SAMPLE_SIZE):

        intr_caught.append(single_sample("RANDOM"))

    return (mean(intr_caught), round(stdev(intr_caught),DECIMAL_PLACES))


main()