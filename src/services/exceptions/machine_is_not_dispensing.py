class MachineIsNotDispensingException(Exception):
    def __init__(self):
        message = "machine is not DISPENSING for operation"
        super().__init__(message)
