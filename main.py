from intruder import Intruder
from aircraft import Aircraft
from statistics import mean, stdev
from math import sqrt
from numpy import arange

"""These properties are my assumptions """

# Channel Properties
CHANNEL_X = 100
CHANNEL_Y = 50

# Aircraft Properties
AIRCRAFT_SPEED = 3
AIRCRAFT_STARTING_X = 50
AIRCRAFT_STARTING_Y = 0
SENSOR_RANGE = 3

# Intruder properties
INTRUDER_SPEED = 2

# Other properties
DECIMAL_PLACES = 2
NUM_OF_INTRUDERS = 100
SAMPLE_SIZE = 100
STEP_SIZE = 0.2

def main():

    prob, velocity, stddev = find_optimal_straight_path()
    print(f"The optimal route to take is with a horizontal velocity of {velocity}")
    print(f"and a vertical velocity of {sqrt(AIRCRAFT_SPEED ** 2 - velocity ** 2)}")
    print(f"This gives a {prob} probability of successfully locating the intruder")
    print(f"with a standard deviation of {stddev}")


def single_intruder(aircraft, intruder):

    # Move intruder and aircraft until caught or intruder has reached the end
    while intruder.x_pos < CHANNEL_X:
        aircraft.move()
        intruder.move()

        if aircraft.check_intruder(intruder):

            return True

    return False


def multiple_intruder(x_speed):
    
    # Keep count of number of intruders caught
    intruders_caught = 0

    # Create loop for number of intruders
    for _ in range(NUM_OF_INTRUDERS):

        # Create instance of aircraft
        aircraft = Aircraft(speed=AIRCRAFT_SPEED,
                    x_pos=AIRCRAFT_STARTING_X,
                    y_pos=AIRCRAFT_STARTING_Y,
                    sensor_range=SENSOR_RANGE,
                    channel_x=CHANNEL_X,
                    channel_y=CHANNEL_Y,
                    x_speed=x_speed)

        # Create instance of intruder
        intruder = Intruder(speed=INTRUDER_SPEED,
                    channel_x=CHANNEL_X,
                    channel_y=CHANNEL_Y)

        # Add to intruder count if caught
        if single_intruder(aircraft, intruder):
            intruders_caught += 1

    return intruders_caught / NUM_OF_INTRUDERS

def stats(x_speed):

    # Collect samples of probability of catching intruders
    samples = [
        multiple_intruder(x_speed)
        for _ in range(SAMPLE_SIZE)
    ]

    # Calculate average and standard deviation from samples
    avg = round(mean(samples), DECIMAL_PLACES)
    std = round(stdev(samples), DECIMAL_PLACES)

    return (avg, std)


def find_optimal_straight_path():

    max_prob = 0
    max_x_speed = 0
    max_std = 0

    # Loop through a range of horizontal velocity to determine optimal
    for x_speed in arange(-AIRCRAFT_SPEED, AIRCRAFT_SPEED+STEP_SIZE, STEP_SIZE):
        prob, std = stats(x_speed)

        print(f"Prob is {prob} for a horizontal velocity of {round(x_speed, 2)}")
        # Store the horizontal velocity with the highest probability
        if prob > max_prob:
            max_prob = prob
            max_x_speed = x_speed
            max_std = std

    return (max_prob, max_x_speed, max_std)

main()