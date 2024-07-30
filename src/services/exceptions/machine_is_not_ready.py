class MachineIsNotReadyException(Exception):
    def __init__(self):
        message = "machine is not READY for operation"
        super().__init__(message)
