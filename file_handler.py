import os
from account import Account, SubsidiaryLedger


def write_account_to_file(accounts):
    file_path = "accounts.txt"

    try:
        with open(file_path, "w") as file:
            for account in accounts.values():
                account_data = {"name": account.name, "code": account.code}
                subsidiary_ledgers = []
                for ledger in account.subsidiary_ledgers:
                    subsidiary_ledgers.append({"name": ledger.name, "code": ledger.code})
                account_data["subsidiary_ledgers"] = subsidiary_ledgers
                file.write(str(account_data) + "\n")
    except IOError:
        print("Error writing to the file.")


def read_accounts_from_file():
    accounts = {}

    file_path = "accounts.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                account_data = eval(line.strip())
                account = Account(account_data['name'], account_data['code'])
                if 'subsidiary_ledgers' in account_data:
                    subsidiary_ledgers = account_data['subsidiary_ledgers']
                    for subsidiary_ledger_data in subsidiary_ledgers:
                        subsidiary_ledger = SubsidiaryLedger(subsidiary_ledger_data['name'],
                                                             subsidiary_ledger_data['code'])
                        account.subsidiary_ledgers.append(subsidiary_ledger)
                accounts[account.code] = account

    return accounts
