from math import sqrt, cos, sin, pi


class Aircraft:

    def __init__(self, speed, x_pos, y_pos, sensor_range, 
                 channel_x, channel_y, x_speed):
        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sensor_range = sensor_range
        self.channel_x = channel_x
        self.channel_y = channel_y
        self.x_speed = x_speed
        self.y_speed = self.get_y_speed()

    def move(self):

    # Handles login for pathtype
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

    # If current coordinates exceeds the channel,
    # bring it back into range and reverse direction
        if self.x_pos < 0:
            self.x_pos = abs(self.x_pos)
            self.x_speed = -self.x_speed

        elif self.x_pos > self.channel_x:
            self.x_pos = 2 * self.channel_x - self.x_pos
            self.x_speed = -self.x_speed

        if self.y_pos < 0:
            self.y_pos = abs(self.y_pos)
            self.y_speed = -self.y_speed

        elif self.y_pos > self.channel_y:
            self.y_pos = 2 * self.channel_y - self.y_pos
            self.y_speed = -self.y_speed

    # Calculate y_speed using pythogoras theorem
    def get_y_speed(self):
        return sqrt(self.speed ** 2 - self.x_speed ** 2)

    # Check if intruder in range
    def check_intruder(self, intruder):

        if abs(self.x_pos - intruder.x_pos) <= 5 and abs(self.y_pos - intruder.y_pos) <= 5:
            return True

        return False
