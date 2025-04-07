import csv

income_file = "income.csv"
expense_file = "expense.csv"

class TransactionManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_transaction(self, transaction):
        with open(self.file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(transaction)

    def read_transactions(self):
        try:
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)
                return list(reader)
        except FileNotFoundError:
            return []

def balance_calculator(income_manager, expense_manager, end_date=None):
    incomes = income_manager.read_transactions()
    expenses = expense_manager.read_transactions()

    total_income = sum(float(transaction[0]) for transaction in incomes if end_date is None or transaction[1] <= end_date)
    total_expense = sum(float(transaction[0]) for transaction in expenses if end_date is None or transaction[1] <= end_date)

    return total_income - total_expense
    
def income_calculator(income_manager, expense_manager, end_date=None):
    incomes = income_manager.read_transactions()

    total_income = sum(float(transaction[0]) for transaction in incomes if end_date is None or transaction[1] <= end_date)

    return total_income
    
def expense_calculator(income_manager, expense_manager, end_date=None):
    expenses = expense_manager.read_transactions()

    total_expense = sum(float(transaction[0]) for transaction in expenses if end_date is None or transaction[1] <= end_date)

    return total_expense
