class Account:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.subsidiary_ledgers = []

    def __str__(self):
        return f"Account: {self.name} (Code: {self.code})"


class SubsidiaryLedger:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __str__(self):
        return f"Subsidiary Ledger: {self.name} (Code: {self.code})"
