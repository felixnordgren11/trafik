
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
        self.lane_right = tc.Lane(6)
        self.light_west = tc.Light(14,6)
        self.light_south = tc.Light(14,4)
        self.dest_gen = des.DestinationGenerator()
        self.line = []
        
        self.stats = {
            'vehicles_created' : 0,
            'vehicles_in_system' : 0,
            'vehicles_out' : {'west': 0, 'south' : 0},
            'mean_time' : {'west': 0, 'south' : 0},
            'median_time' : {'west': 0, 'south' : 0},
            'min_time' : {'west': 0, 'south' : 0},
            'max_time' : {'west': 0, 'south' : 0},
            'blocked_time' : 0,
            'queue_time' : 0
        }
    '''
    def snapshot(self):
        """
        Print a snap shot of the current state of the system.
        """
        #print(f'Time step {self.time}')
        if TrafficSystem.hold_sign(self) is not None:
            print(f'{self.light_west}{self.lane_west.__str__()} {TrafficSystem.hold_sign2(self)} {self.lane_right.__str__()} {self.line}')
            print(f'{self.light_south}{self.lane_south}')
        else:
            print(f'{self.light_west}{self.lane_west.__str__()} {self.lane_right.__str__()} {self.line}')
            print(f'{self.light_south}{self.lane_south}')
        
    def hold_sign2(self):
        if all(vehicle is not None for vehicle in self.lane_west.lane_slot) and tc.Lane.get_first(self.lane_right) == 'W':
            return '*'
        elif all(vehicle is not None for vehicle in self.lane_south.lane_slot) and tc.Lane.get_first(self.lane_right) == 'S':
            return '*'
        else:
            pass
    '''
    def snapshot(self):
        """
        Print a snap shot of the current state of the system.
        """
        if self.should_hold_sign():
            print(f'{self.light_west}{self.lane_west} * {self.lane_right} {self.line}')
        else:
            print(f'{self.light_west}{self.lane_west} {self.lane_right} {self.line}')
        print(f'{self.light_south}{self.lane_south}')

    def should_hold_sign(self):
        """
        Check if the * sign should be printed.
        """
        right_lane_first_direction = tc.Lane.get_first(self.lane_right)
        if right_lane_first_direction is not None:
            rld = right_lane_first_direction.destination
        if all(vehicle is not None for vehicle in self.lane_west.lane_slot) and rld == 'W':
            self.stats['blocked_time'] += 1
            return True
        elif all(vehicle is not None for vehicle in self.lane_south.lane_slot) and rld == 'S':
            self.stats['blocked_time'] += 1
            return True
        return False


    
    def swlane_step(self):
        if tc.Light.is_green(self.light_west) and tc.Lane.get_first(self.lane_west):
            self.lane_west.remove_first()
            self.stats['vehicles_out']['west'] += 1
        if tc.Light.is_green(self.light_south) and tc.Lane.get_first(self.lane_south):
            self.lane_south.remove_first()
            self.stats['vehicles_out']['south'] += 1
        self.lane_west.step()
        self.lane_south.step()
        
    def right_lane_step(self):
        first_right = self.lane_right.lane_slot[0]
        frd = None
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
        if dir is not None:
            self.line.append(dir)
            #print(f"Before adding - Right Lane: {self.lane_right}")
            if self.lane_right.lane_slot[-1] is None:
                #print(f'{self.lane_right.lane_slot[-1] == None}')
                line0 = self.line.pop(0)
                vehicle = tc.Vehicle(line0, self.time)
                self.lane_right.enter(vehicle)
        elif self.line and self.lane_right.lane_slot[-1] is None:
            line0 = self.line.pop(0)
            vehicle = tc.Vehicle(line0, self.time)
            self.lane_right.enter(vehicle)
        self.light_south.step()
        self.light_west.step()
        
        
    
    def print_statistics():
        pass
                
            
        
        

            
            
        

def main():
    ts = TrafficSystem()
    for _ in range(300):
        ts.snapshot()
        ts.step()
        sleep(0.01) # Pause for 0.1 s.
    print('\nFinal state:')
    ts.snapshot()
    print()


if __name__ == '__main__':
    main()