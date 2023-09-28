
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
        self.light = tc.Light(9,6)
        self.dest_gen = des.DestinationGenerator()
        self.line = []

    def snapshot(self):
        """Print a snap shot of the current state of the system."""
        #print(f'Time step {self.time}')
        print(f'{self.left_lane.__str__()} {self.light.__str__()} {self.right_lane.__str__()} {self.line}')
        

    def step(self):
        """Take one time step for all components."""
        self.time += 1
        if self.left_lane is not None:
            self.left_lane.remove_first()
        self.left_lane.step()
        if self.light.is_green() == True and self.right_lane.lane_slot[0] is not None:
            self.left_lane.enter(self.right_lane.lane_slot[0])
            self.right_lane.remove_first()
        self.light.step()
        self.right_lane.step()
        dir = self.dest_gen.step()
        #print(f"Direction: {dir}")
        l = self.right_lane.lane_slot[0]
        if l is not None:
            print(l.destination)
            
        
        if dir is not None:
            self.line.append(dir)
            if self.right_lane.lane_slot[-1] is None:
                line0 = self.line.pop(0)
                vehicle = tc.Vehicle(line0, self.time)
                self.right_lane.enter(vehicle)
        else:
            if self.line and self.line[0] is not None:
                if self.right_lane.lane_slot[-1] is None:
                    line1 = self.line.pop(0)
                    vehicle = tc.Vehicle(line1, self.time)
                    self.right_lane.enter(vehicle)
            
            
        
        '''    
        if all(vehicle is not None for vehicle in self.right_lane.lane_slot) and self.light.is_green == False:
        occ = self.right_lane.lane_slot[-1]
        if occ is None and self.line:
            vehicle = tc.Vehicle(self.line[0], self.time)
            self.right_lane.enter(self.line[0])
            del self.line[0]
        '''

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