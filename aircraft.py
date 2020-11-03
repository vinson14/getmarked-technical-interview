import math
import random

class Aircraft:

    def __init__(self, speed, x_pos, y_pos, sensor_range, channel_x, channel_y):

        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sensor_range = sensor_range
        self.channel_x = channel_x
        self.channel_y = channel_y

        # Parameters for zigzag
        self.x_speed = None

        # Parameters for circular movement
        self.radius = None
        self.center = None
        self.radian = None
        self.omega = None

    def move_circular(self, radius):
        
        if self.radius is None:
            
            # Check that radius of circle does not exceed channel
            if self.y_pos + 2 * radius > self.channel_y:
                raise Exception("Radius causes circular motion to exceed channel")
            
            # Sets the parameters for circular motion
            self.radius = radius
            self.center = (self.x_pos, self.y_pos + radius)
            self.radian = math.pi

            self.omega = self.speed / self.radius

        # Moves to new position
        self.radian += self.omega
        self.x_pos = self.center[0] + self.radius * math.sin(self.radian)
        self.y_pos = self.center[1] + self.radius * math.cos(self.radian)


    def move_zigzag(self, x_speed):

        if self.x_speed is None:
            self.x_speed = x_speed

            # Calculate y_speed using pythogoras theorem
            self.y_speed = math.sqrt(self.speed ** 2 - self.x_speed ** 2)

        # Move aircraft to new position
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

        # Ensure aircraft does not exceed boundaries
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

    # Move in a random manner
    def move_random(self):

        # Get random x_speed
        rand_x_speed = random.randint(-self.speed, self.speed)

        # Calculate y_speed using pythogoras theorem
        rand_y_speed = math.sqrt(self.speed ** 2 - rand_x_speed ** 2)

        # Move aircraft to new position
        self.x_pos += rand_x_speed
        self.y_pos += rand_y_speed

        # Ensure aircraft does not exceed boundaries
        if self.x_pos < 0:
            self.x_pos = abs(self.x_pos)
        
        elif self.x_pos > self.channel_x:
            self.x_pos = 2 * self.channel_x - self.x_pos

        if self.y_pos < 0:
            self.y_pos = abs(self.y_pos)
        
        elif self.y_pos > self.channel_y:
            self.y_pos = 2 * self.channel_y - self.y_pos


    # Check if intruder in range
    def check_intruder(self, intruder):

        if abs(self.x_pos - intruder.x_pos) <= 5 and abs(self.y_pos - intruder.y_pos) <= 5:
            return True

        return False