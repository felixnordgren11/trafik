
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
        self.left_lane = tc.Lane(5)
        self.right_lane = tc.Lane(5)
        self.light = tc.Light(7,3)
        self.dest_gen = des.DestinationGenerator()

    def snapshot(self):
        """Print a snap shot of the current state of the system."""
        print(f'Time step {self.time}')
#        for l in [self.left_lane, self.right_lane]:
#            print(f'[' + ''.join([vehicle.destination if vehicle is not None else '.' for vehicle in l]) + ']')
        

    def step(self):
        """Take one time step for all components."""
        self.time += 1
        if self.left_lane is not None:
            tc.Lane.remove_first(self)
        self.left_lane.step()
        if self.light.is_green() == True and self.right_lane[0] is not None:
            self.left_lane[-1] = self.right_lane[0]
        self.light.step()
        self.right_lane.step()
        des.DestinationGenerator.step()
            


def main():
    ts = TrafficSystem()
    for _ in range(100):
        ts.snapshot()
        ts.step()
        sleep(0.1) # Pause for 0.1 s.
    print('\nFinal state:')
    ts.snapshot()
    print()


if __name__ == '__main__':
    main()