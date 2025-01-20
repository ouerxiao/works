
"""
The new tire wear sensors produce an array of four numbers between 0 and 1 inclusive, representing how worn each of the tires are. 
This array will be passed to each function in the car factory class, to be used by your tire implementation. 

Carrigan tires should be serviced only when one or more of the values in the tire wear array is greater than or equal to 0.9.
"""

from tires.tires import Tires


class CarriganTires(Tires):
    def __init__(self, tire_wear):
        self.tire_wear = tire_wear

    def needs_service(self):
        for tire in self.tire_wear:
            if tire >= 0.9:
                return True
        return False