


class Vehicle:
    """Represents vehicles in traffic simulations"""

    def __init__(self, destination, borntime):
        """Creates the vehicle with specified properties."""
        self.destination = destination
        self.borntime = borntime
        self.name = 'Vehicle'
    
    def __str__(self):
        return self.name + f'({self.destination}, {self.borntime})'


class Lane:
    """Represents a lane with (possibly) vehicles"""

    def __init__(self, length):
        """Creates a lane of specified length."""
        self.length = length
        self.lane_slot = [None for _ in range(length)]
        self.time = 0
        

    def __str__(self):
        '''
        String representation of lane
        '''
        #return '[' + ''.join([vehicle.destination if vehicle is not None else '.' for vehicle in self.lane_slot]) + ']'
        return '[' + ''.join([vehicle.destination if isinstance(vehicle, Vehicle) else '.' for vehicle in self.lane_slot]) + ']'

    def enter(self, vehicle):
        """
        Called when a new vehicle enters the end of the lane.
        """
        #print(f"Adding vehicle {vehicle} to lane")
        self.lane_slot[-1] = vehicle
        
        #

    def last_free(self):
        """
        Reports whether there is space for a vehicle at the
        end of the lane.
        """
        if not self.lane_slot[-1] == None:
            return ("Last space is occupied")
        else:
            return("Last space is free")
        #

    def step(self):
        """
        Execute one time step.
        """
        for pos in range(1, self.length):
            if self.lane_slot[pos - 1] is None and self.lane_slot[pos] is not None:
                self.lane_slot[pos - 1] = self.lane_slot[pos]
                self.lane_slot[pos] = None
        #

    def get_first(self):
        """
        Return the first vehicle in the lane, or None.
        """
        return self.lane_slot[0]
        
    
    def get_last(self):
        """
        Return the first vehicle in the lane, or None.
        
        if not self.lane_slot[-1] == None:
            return self.lane_slot[-1]
        else:
            return None
        """
        return self.lane_slot[-1]
        #

    def remove_first(self):
        """Remove the first vehicle in the lane.
           Return the vehicle removed.
           If no vehicle is a the front of the lane, returns None
           without removing anything."""
        removed_vehicle = self.lane_slot[0]
        self.lane_slot[0] = None
        return removed_vehicle
            

    def number_in_lane(self):
        """Return the number of vehicles currently in the lane."""
        _num = 0
        for pos in self.lane_slot:
            if not pos == None:
                _num += 1
        return _num
            
        #
        
        
def demo_lane():
    """For demonstration of the class Lane"""
    a_lane = Lane(10)
    print(a_lane)
    v = Vehicle('N', 34)
    a_lane.enter(v)
    print(a_lane)

    a_lane.step()
    print(a_lane)
    for i in range(20):
        if i % 2 == 0:
            u = Vehicle('S', i)
            a_lane.enter(u)
        a_lane.step()
        print(a_lane)
        if i % 3 == 0:
            print('  out: ',
                  a_lane.remove_first())
    print('Number in lane:',
          a_lane.number_in_lane())





class Light:
    """Represents a traffic light"""

    def __init__(self, period, green_period):
        """Create a light with the specified timers."""
        self.period = period
        self.green_period = green_period
        self.time = 0
        self.green = True
        
    # uppdatera alla komponenter
    # presentera tillståndet (eventuellt)
        #.

    def __str__(self):
        """Report current state of the light."""
        if not self.green == True:
            return ('(R)')
        else:
            return('(G)')
        

    def step(self):
        """Take one light time step."""
        self.time += 1
        if self.time % self.period >= self.green_period:
            self.green = False
        else:
            self.green = True
            

    def is_green(self):
        """Return whether the light is currently green."""
        if self.green == True:
            return True
        else:
            return False
        
            
        
def demo_light():
    """Demonstrats the Light class"""
    a_light = Light(7, 3)
    for i in range(15):
        print(i, a_light,
              a_light.is_green())
        a_light.step()

def main():
    """Demonstrates the classes"""
    print('\nLight demonstration\n')
    demo_light()
    print('\nLane demonstration')
    demo_lane()

if __name__ == '__main__':
    main()