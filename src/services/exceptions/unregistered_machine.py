class UnregisteredMachineException(Exception):
    def __init__(self, id: str):
        message = 'machine - "' + id + '" - is not registered in the system'
        super().__init__(message)
