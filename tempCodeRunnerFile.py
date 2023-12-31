
from statistics import mean, median
from time import sleep
import destinations as des
import trafficComponents as tc


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):
        """Initialize all components of the traffic
        system."""
        self.time = 0
        self.lane_west = tc.Lane(4)
        self.lane_south = tc.Lane(4)
        self.lane_right = tc.Lane(5)
        self.light_west = tc.Light(9,6)
        self.light_south = tc.Light(9,6)
        self.dest_gen = des.DestinationGenerator()
        self.line = []

    def snapshot(self):
        """Print a snap shot of the current state of the system."""
        #print(f'Time step {self.time}')
        print(f'{self.light_west}{self.lane_west.__str__()} {self.lane_right.__str__()} {self.line}')
        print(f'{self.light_south}{self.lane_south}')
        

    def step(self):
        if self.light_west.is_green == True:
            self.lane_west.remove_first()
        if self.light_south.is_green == True:
            self.lane_south.remove_first()
        self.lane_west.step()
        self.lane_south.step()
        first_right = self.lane_right.lane_slot[0]
        frd = None
        if first_right is not None and first_right.direction is not None:
            frd = first_right.direction
        if frd is not None:
            if frd is 'W':
                self.lane_west.enter(first_right)
            else:
                self.lane_south.enter(first_right)
            self.lane_right.remove_first()
        dir = self.dest_gen.step()
        if dir is not None:
            self.line.append(dir)
            if self.lane_right.lane_slot[-1] is None:
                line0 = self.line.pop(0)
                vehicle = tc.Vehicle(line0, self.time)
                self.lane_right.enter(vehicle)
        
        self.lane_right.step()