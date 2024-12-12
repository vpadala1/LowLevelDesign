class Elevator:
    def __init__(self, name):
        self.name = "Elevator" + name

    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name