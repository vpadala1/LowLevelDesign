class ElevatorButtons:
    _instance = None 

    def __init__(self,floors):
        if self._instance is not None:
            raise Exception("Already Created the instance!!!")
        self.floor = floors

    def get_instance(self, floors = 10):
        if self._instance is None:
            ElevatorButtons(floors)
        return self._instance

    def pressButton(self, dest_floor):
        pass
        