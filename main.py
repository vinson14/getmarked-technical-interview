from intruder import Intruder
from aircraft import Aircraft
from statistics import mean, stdev
from numpy import arange
import math

"""These properties are my assumptions
    These values can be changed and the code would still work
"""

# Channel Properties
CHANNEL_X = int(input("Length of Channel: "))
CHANNEL_Y = int(input("Width of Channel: "))

# Aircraft Properties
AIRCRAFT_SPEED = int(input("Speed of aircraft: "))
AIRCRAFT_STARTING_X = CHANNEL_X // 2
AIRCRAFT_STARTING_Y = 0
SENSOR_RANGE = int(input("Range of Sensor: "))

# Intruder properties
INTRUDER_SPEED = int(input("Speed of Intruder: "))

# Other properties
DECIMAL_PLACES = 2
NUM_OF_INTRUDERS = 100
SAMPLE_SIZE = int(input("Sample size: "))
STEP_SIZE = float(input("Step size of testing: "))


def main():

    if AIRCRAFT_STARTING_X > CHANNEL_X or AIRCRAFT_STARTING_Y > CHANNEL_Y:
        print("Please ensure that the aircraft's starting position is correct")
        return

    prob, velocity, stddev = find_optimal_straight_path()
    print(f"Optimal horizontal velocity: {round(velocity,2)}\nProbability of success: {prob}")


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
    for x_speed in arange(-AIRCRAFT_SPEED, AIRCRAFT_SPEED, STEP_SIZE):
        prob, std = stats(x_speed)

        # Store the horizontal velocity with the highest probability
        if prob > max_prob:
            max_prob = prob
            max_x_speed = x_speed
            max_std = std

    return (max_prob, max_x_speed, max_std)


main()
