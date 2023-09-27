
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
        #print(f'Time step {self.time}')
        print(f'{self.left_lane.__str__()} {self.right_lane.__str__()}')
        

    def step(self):
        """Take one time step for all components."""
        self.time += 1
        if self.left_lane is not None:
            self.left_lane.remove_first()
        self.left_lane.step()
        if self.light.is_green() == True and self.right_lane[0] is not None:
            self.left_lane[-1] = self.right_lane[0]
        self.light.step()
        self.right_lane.step()
        self.dest_gen.step()
        if self.dest_gen is not None:
            tc.Lane.enter(self.dest_gen.step())
        
            


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