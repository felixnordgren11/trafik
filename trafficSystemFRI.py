
from statistics import mean, median
from time import sleep
import destinations as des
import trafficComponents as tc


class TrafficSystem:
    """
    Defines a traffic system
    """

    def __init__(self):
        """
        Initialize all components of the traffic
        system.
        """
        self.time = 0
        self.lane_west = tc.Lane(4)
        self.lane_south = tc.Lane(4)
        self.lane_right = tc.Lane(5)
        self.light_west = tc.Light(9,4)
        self.light_south = tc.Light(9,3)
        self.dest_gen = des.DestinationGenerator()
        self.line = []

    def snapshot(self):
        """
        Print a snap shot of the current state of the system.
        """
        #print(f'Time step {self.time}')
        print(f'{self.light_west}{self.lane_west.__str__()} {self.lane_right.__str__()} {self.line}')
        print(f'{self.light_south}{self.lane_south}')
        

    def step(self):
        '''
        Steps the whole system.
        '''
        if tc.Light.is_green(self.light_west) == True:
            self.lane_west.remove_first()
        if tc.Light.is_green(self.light_south) == True:
            self.lane_south.remove_first()
        self.lane_west.step()
        self.lane_south.step()
        first_right = self.lane_right.lane_slot[0]
        frd = None
        if first_right is not None:
            frd = first_right.destination
    
        if frd is not None:
            if frd == 'W':
                self.lane_west.enter(first_right)
            else:
                self.lane_south.enter(first_right)
            self.lane_right.remove_first()
        self.lane_right.step()
            
        dir = self.dest_gen.step()
        if dir is not None:
            self.line.append(dir)
            if self.lane_right.lane_slot[-1] is None:
                line0 = self.line.pop(0)
                vehicle = tc.Vehicle(line0, self.time)
                self.lane_right.enter(vehicle)
        
        
        
        
        
        
        self.light_south.step()
        self.light_west.step()
                
            
        
        

            
            
        

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