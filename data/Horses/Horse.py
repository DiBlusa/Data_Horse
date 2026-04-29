import math


class Horse:
    def __init__(self, name, time, theta_deg, distance=100):
        self.name = name          # stores the horse's name
        self.distance = distance  # stores the distance traveled
        self.time = time          # stores the time spent
        self.theta_deg = theta_deg  # stores the angle in degrees

    @property
    def speed(self):
        if self.time == 0:
            return 0              # avoids division by zero
        theta_rad = math.radians(self.theta_deg)
        return (self.distance / self.time) * math.sin(theta_rad)  # calculates the speed

