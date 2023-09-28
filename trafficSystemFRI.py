
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
        self.lane_west = tc.Lane(5)
        self.lane_south = tc.Lane(5)
        self.lane_right = tc.Lane(7)
        self.light_west = tc.Light(9,3)
        self.light_south = tc.Light(9,1)
        self.dest_gen = des.DestinationGenerator()
        self.line = []

    def snapshot(self):
        """
        Print a snap shot of the current state of the system.
        """
        #print(f'Time step {self.time}')
        print(f'{self.light_west}{self.lane_west.__str__()} {self.lane_right.__str__()} {self.line}')
        print(f'{self.light_south}{self.lane_south}')
        
    
    def swlane_step(self):
        if tc.Light.is_green(self.light_west) == True:
            self.lane_west.remove_first()
        if tc.Light.is_green(self.light_south) == True:
            self.lane_south.remove_first()
        self.lane_west.step()
        self.lane_south.step()
        
    def right_lane_step(self):
        first_right = self.lane_right.lane_slot[0]
        frd = None
        print(tc.Lane.get_last(self.lane_west))
        if first_right is not None:
            frd = first_right.destination
        if frd is not None:
            if frd == 'W' and tc.Lane.get_last(self.lane_west) is None:
                self.lane_west.enter(first_right)
                self.lane_right.remove_first()
            elif frd == 'S' and tc.Lane.get_last(self.lane_south) is None:
                self.lane_south.enter(first_right)
                self.lane_right.remove_first()
        self.lane_right.step()
        

    def step(self):
        '''
        Steps the whole system.
        '''
        self.swlane_step()
        self.right_lane_step()
        dir = self.dest_gen.step()
        print(dir)
        if dir is not None:
            self.line.append(dir)
            #print(f"Before adding - Right Lane: {self.lane_right}")
            if self.lane_right.lane_slot[-1] is None:
                print(f'{self.lane_right.lane_slot[-1] == None}')
                line0 = self.line.pop(0)
                vehicle = tc.Vehicle(line0, self.time)
                self.lane_right.enter(vehicle)
        elif self.line:
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