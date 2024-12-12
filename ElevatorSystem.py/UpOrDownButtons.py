from ElevatorManager import ElevatorManager

class UpOrDownButtons:
    def __init__(self):
        pass

    def pressButton(self, direction):
        
        elevatorManagerInstace = ElevatorManager.get_instance()
        idleElevator = elevatorManagerInstace.findElevator(self, direction)