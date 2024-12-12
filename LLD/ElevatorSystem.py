"""

1. User comes to an elevator and at external board he presses up or down arrow based on which an elevator car comes to him.
2. Once he went into elevator car he can choose the floor he want to move to.
3. Car has two traits, STATE:- IDLE, MOVING , DIRECTION:- UP, DOWN
4. 


1. Elevator -> State(IDLE,MOVING), Direction(UP,DOWN), FloorsToStop(EntriesfromInside, minHeap is used when moving Up and maxHeap when moving Down), DoorsOpen, DoorsClose, 
                   MaxWeightAchieved(Elevator is Stopped at the same floor, An Alarm is buzzed)
2. Elevator Controller -> n - Elevators, getQuickestOne()
"""

from enum import Enum

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"


class ElevatorState(Enum):
    MOVING = "MOVING"
    IDLE = "IDLE"

class ElevatorDisplay:
    def __init__(self):
        self.floor = None
        self.direction = None

    def set_display(self, floor, direction):
        self.floor = floor
        self.direction = direction

    def show_display(self):
        print(f"Floor: {self.floor}")
        print(f"Direction: {self.direction}")


class ElevatorDoor:
    def open_door(self):
        print("Opening the Elevator door")

    def close_door(self):
        print("Closing the Elevator door")


class ElevatorCar:
    def __init__(self, car_id):
        self.id = car_id
        self.display = ElevatorDisplay()
        self.internal_buttons = InternalButtons()
        self.elevator_state = ElevatorState.IDLE
        self.current_floor = 0
        self.elevator_direction = Direction.UP
        self.elevator_door = ElevatorDoor()

    def show_display(self):
        self.display.show_display()

    def press_button(self, destination):
        self.internal_buttons.press_button(destination, self)

    def set_display(self):
        self.display.set_display(self.current_floor, self.elevator_direction)

    def move_elevator(self, direction, destination_floor):
        start_floor = self.current_floor
        if direction == Direction.UP:
            for i in range(start_floor, destination_floor + 1):
                self.current_floor = i
                self.set_display()
                self.show_display()
                if i == destination_floor:
                    return True

        if direction == Direction.DOWN:
            for i in range(start_floor, destination_floor - 1, -1):
                self.current_floor = i
                self.set_display()
                self.show_display()
                if i == destination_floor:
                    return True

        return False


class ElevatorController:
    def __init__(self, elevator_car):
        self.up_min_pq = []
        self.down_max_pq = []
        self.elevator_car = elevator_car

    def submit_external_request(self, floor, direction):
        if direction == Direction.DOWN:
            self.down_max_pq.append(floor)
            self.down_max_pq.sort(reverse=True)
        else:
            self.up_min_pq.append(floor)
            self.up_min_pq.sort()

    def submit_internal_request(self, floor):
        # Implementation for handling internal requests can be added here
        pass

    def control_elevator(self):
        while True:
            if self.elevator_car.elevator_direction == Direction.UP:
                if self.up_min_pq:
                    next_floor = self.up_min_pq.pop(0)
                    self.elevator_car.move_elevator(Direction.UP, next_floor)
            elif self.elevator_car.elevator_direction == Direction.DOWN:
                if self.down_max_pq:
                    next_floor = self.down_max_pq.pop(0)
                    self.elevator_car.move_elevator(Direction.DOWN, next_floor)


class ElevatorCreator:
    elevator_controller_list = []

    @staticmethod
    def create_elevators():
        elevator_car1 = ElevatorCar(1)
        controller1 = ElevatorController(elevator_car1)
        ElevatorCreator.elevator_controller_list.append(controller1)

        elevator_car2 = ElevatorCar(2)
        controller2 = ElevatorController(elevator_car2)
        ElevatorCreator.elevator_controller_list.append(controller2)


class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.external_dispatcher = ExternalDispatcher()

    def press_button(self, direction):
        self.external_dispatcher.submit_external_request(self.floor_number, direction)


class Building:
    def __init__(self, floors):
        self.floor_list = floors

    def add_floors(self, new_floor):
        self.floor_list.append(new_floor)

    def remove_floors(self, remove_floor):
        self.floor_list.remove(remove_floor)

    def get_all_floor_list(self):
        return self.floor_list


class ExternalDispatcher:
    def __init__(self):
        self.elevator_controller_list = ElevatorCreator.elevator_controller_list

    def submit_external_request(self, floor, direction):
        for elevator_controller in self.elevator_controller_list:
            elevator_id = elevator_controller.elevator_car.id
            if (elevator_id % 2 == 1 and floor % 2 == 1) or (elevator_id % 2 == 0 and floor % 2 == 0):
                elevator_controller.submit_external_request(floor, direction)


class InternalButtons:
    def __init__(self):
        self.dispatcher = InternalDispatcher()

    def press_button(self, destination, elevator_car):
        self.dispatcher.submit_internal_request(destination, elevator_car)


class InternalDispatcher:
    def __init__(self):
        self.elevator_controller_list = ElevatorCreator.elevator_controller_list

    def submit_internal_request(self, floor, elevator_car):
        # Implementation for handling internal requests can be added here
        pass


if __name__ == "__main__":
    # Create elevators
    ElevatorCreator.create_elevators()

    # Create building floors
    floor_list = [Floor(i) for i in range(1, 6)]

    # Create the building
    building = Building(floor_list)

    # Simulate pressing buttons on various floors
    floor_list[0].press_button(Direction.UP)
    floor_list[1].press_button(Direction.DOWN)
    floor_list[2].press_button(Direction.UP)
    floor_list[3].press_button(Direction.DOWN)
    floor_list[4].press_button(Direction.UP)
