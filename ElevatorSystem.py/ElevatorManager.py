from Elevator import Elevator
from collections import deque
from threading import Lock
from ElevatorStatus import ElevatorStatus

class ElevatorManager:
    _instance = None
    _lock = Lock()
    def __init__(self, noOfElevators):
        if self._instance is not None:
            raise Exception("Use get_instance() method not this way. An instance already exists.")
        self.requests = deque()
        self.elevators = [Elevator(i+1) for i in range(noOfElevators)]
    
    @staticmethod
    def get_instance(cls, noOfElevators = 4):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls(noOfElevators)
        return cls._instance
    
    def findElevator(self):

        ## Sending an idle elevator for now we can extend it to Moving ones...
        for elevator in self.elevators:
            if elevator.status == ElevatorStatus.IDLE:
                return elevator
            


