from random import randint

class Intruder():

    def __init__(self, speed, channel_x, channel_y, x_pos=0):
        self.speed = speed
        self.x_pos = x_pos
        self.channel_x = channel_x
        self.channel_y = channel_y

        # Randomly assign y position to intruder
        self.y_pos = randint(0, channel_y)


    # Function to move intruder
    def move(self):
        self.x_pos += self.speed