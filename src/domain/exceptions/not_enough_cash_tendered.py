class NotEnoughCashTenderedException(Exception):
    def __init__(self, amount: int, cash_tendered: int):
        message = 'cash tendered of - ' + str(cash_tendered) + ' - is not enough to pay the amount of - ' + str(amount)
        super().__init__(message)
