from abc import ABC, abstractmethod
from typing import override

class Vehicle():
    def numberOfWheels(self):
        return 2
    
class EngineVehicle(Vehicle):
    def hasEngine(self):
        return True
    
class MotorCycle(EngineVehicle):
    pass

class Car(EngineVehicle):
    def numberOfWheels(self):
        return 4
    
class BiCycle(Vehicle):
    pass 

ListOfVehicles = []
ListOfVehicles.append(MotorCycle())
ListOfVehicles.append(Car())
ListOfVehicles.append(BiCycle())

for vehicle in ListOfVehicles:
    print(vehicle.numberOfWheels())

"""

So Liskov Substition principle says that Children should be able to replace its parent by having more properties thats okay
But..  It shouldn't forgot the property that it parent holds and it should never forget inheriting it..

Also.. In the above code we can see BiCycle doesn't have an engine but it can still replace parent as the Vehicle class also doesn't have engine
But.. Both carry the same set of attributes..

"""