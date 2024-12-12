from abc import ABC, abstractmethod
import heapq


# Enum for Direction
class Direction:
    UP = 'UP'
    DOWN = 'DOWN'
    IDLE = 'IDLE'


# Request class to represent a request to the elevator
class Request:
    def __init__(self, destination_floor, direction):
        self.destination_floor = destination_floor
        self.direction = direction


# State interface for the elevator
class ElevatorState(ABC):
    @abstractmethod
    def handle_request(self, elevator, request):
        """Handle requests based on the current state of the elevator."""
        pass

    @abstractmethod
    def move(self, elevator):
        """Move the elevator according to the current state."""
        pass


# Concrete state: IdleState
class IdleState(ElevatorState):
    def handle_request(self, elevator, request):
        # Add request to elevator's list and change state based on direction
        elevator.assign_request(request)
        if request.direction == Direction.UP:
            elevator.set_state(elevator.moving_up_state)
        elif request.direction == Direction.DOWN:
            elevator.set_state(elevator.moving_down_state)

    def move(self, elevator):
        print(f"Elevator {elevator.elevator_id} is idle on floor {elevator.current_floor}. No movement.")


# Concrete state: MovingUpState
class MovingUpState(ElevatorState):
    def handle_request(self, elevator, request):
        if request.direction == Direction.UP:
            elevator.add_up_request(request)
        else:
            elevator.add_down_request(request)

    def move(self, elevator):
        if elevator.up_requests:
            next_floor = heapq.heappop(elevator.up_requests)
            elevator.current_floor = next_floor
            print(f"Elevator {elevator.elevator_id} moving up to floor {next_floor}.")
            if not elevator.up_requests:  # No more upward requests
                elevator.set_state(elevator.idle_state)
        else:
            elevator.set_state(elevator.idle_state)


# Concrete state: MovingDownState
class MovingDownState(ElevatorState):
    def handle_request(self, elevator, request):
        if request.direction == Direction.DOWN:
            elevator.add_down_request(request)
        else:
            elevator.add_up_request(request)

    def move(self, elevator):
        if elevator.down_requests:
            next_floor = -heapq.heappop(elevator.down_requests)
            elevator.current_floor = next_floor
            print(f"Elevator {elevator.elevator_id} moving down to floor {next_floor}.")
            if not elevator.down_requests:  # No more downward requests
                elevator.set_state(elevator.idle_state)
        else:
            elevator.set_state(elevator.idle_state)


# Elevator class
class Elevator:
    def __init__(self, elevator_id, max_capacity):
        self.elevator_id = elevator_id
        self.max_capacity = max_capacity
        self.current_floor = 0
        self.passenger_count = 0
        self.up_requests = []  # Min-heap for upward requests
        self.down_requests = []  # Max-heap for downward requests (using negative values)

        # Define all states
        self.idle_state = IdleState()
        self.moving_up_state = MovingUpState()
        self.moving_down_state = MovingDownState()

        # Start with idle state
        self.current_state = self.idle_state

    def set_state(self, state: ElevatorState):
        """Change the elevator's state."""
        self.current_state = state

    def handle_request(self, request: Request):
        """Delegate the request handling to the current state."""
        self.current_state.handle_request(self, request)

    def move(self):
        """Delegate the move behavior to the current state."""
        self.current_state.move(self)

    def assign_request(self, request: Request):
        """Assign requests based on the direction."""
        if request.direction == Direction.UP:
            heapq.heappush(self.up_requests, request.destination_floor)
        else:
            heapq.heappush(self.down_requests, -request.destination_floor)

    def add_up_request(self, request: Request):
        """Add an upward request to the queue."""
        heapq.heappush(self.up_requests, request.destination_floor)

    def add_down_request(self, request: Request):
        """Add a downward request to the queue."""
        heapq.heappush(self.down_requests, -request.destination_floor)


# Elevator Manager class
class ElevatorManager:
    def __init__(self):
        self.elevators = []

    def add_elevator(self, elevator):
        self.elevators.append(elevator)

    def request_elevator(self, request: Request):
        # For simplicity, assign to the first elevator
        if self.elevators:
            print(f"Request for floor {request.destination_floor} in direction {request.direction}.")
            elevator = self.elevators[0]  # In real implementation, select the best elevator
            elevator.handle_request(request)
            elevator.move()


# Example usage
if __name__ == "__main__":
    # Create elevators
    elevator1 = Elevator(elevator_id=1, max_capacity=5)
    elevator2 = Elevator(elevator_id=2, max_capacity=5)

    # Create elevator manager
    elevator_manager = ElevatorManager()
    elevator_manager.add_elevator(elevator1)
    elevator_manager.add_elevator(elevator2)

    # Simulate requests
    elevator_manager.request_elevator(Request(destination_floor=5, direction=Direction.UP))
    elevator_manager.request_elevator(Request(destination_floor=3, direction=Direction.UP))
    elevator_manager.request_elevator(Request(destination_floor=1, direction=Direction.DOWN))

    # Move elevators
    elevator1.move()
    elevator1.move()
    elevator2.move()
