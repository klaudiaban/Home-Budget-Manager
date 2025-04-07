import customtkinter as ctk
from CTkTable import *
from datetime import datetime
import csv
from budget_manager import *
from ui_helpers import *

def main():
    income_manager = TransactionManager("income.csv")
    expense_manager = TransactionManager("expense.csv")
    income_categories = ["Salary", "Bonus", "Investing", "Gift", "Other"]
    expense_categories = ["Food", "Entertainment", "Transport", "Healthcare", "Other"]
    user_info_file = 'user_info.csv'

    def update_table():
        for widget in table_frame.winfo_children():
            widget.destroy()

        monthly_incomes = [transaction for transaction in income_manager.read_transactions()]
        monthly_expenses = [transaction for transaction in expense_manager.read_transactions()]
        combined_transactions = [(t, "income") for t in monthly_incomes] + [(t, "expense") for t in monthly_expenses]
        sorted_transactions = sort_transactions(combined_transactions)

        create_table(table_frame, sorted_transactions)
        
    def update_labels():
        total_income = income_calculator(income_manager, expense_manager)
        total_expense = expense_calculator(income_manager, expense_manager)
        total_balance = balance_calculator(income_manager, expense_manager)

        amount_income_label.configure(text=str(total_income) + f"{currency}")
        amount_expense_label.configure(text=str(total_expense) + f"{currency}")
        amount_balance_label.configure(text=str(total_balance) + f"{currency}")

    ctk.set_appearance_mode("light")
    window, window_width, window_height = initialize_main_window()

    def read_user_info():
        try:
            with open(user_info_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    return row[0], row[1]
        except FileNotFoundError:
            return None, None
            
    def write_user_info(name, currency):
        with open(user_info_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, currency])
    
    user_name, currency = ask_user_info(window, 'user_info.csv', window_width, window_height)
    window.deiconify()

    def update_name(new_name):
        if new_name:
            user_name, currency = read_user_info()
            write_user_info(new_name, currency)
            update_name_display(new_name)  

    def update_currency(new_currency):
        if new_currency:
            user_name, currency = read_user_info()
            write_user_info(user_name, new_currency)
            update_currency_display(new_currency) 

    def open_name_update_dialog():
        create_name_update_dialog(window, update_name, window_width, window_height)

    def open_currency_update_dialog():
        create_currency_update_dialog(window, update_currency, window_width, window_height)

    def update_name_display(new_name):
        hello_label.configure(text=f"Hello, {new_name}!")

    def update_currency_display(new_currency):
        amount_income_label.configure(text=str(income_calculator(income_manager, expense_manager)) + f" {new_currency}")
        amount_expense_label.configure(text=str(expense_calculator(income_manager, expense_manager)) + f" {new_currency}")
        amount_balance_label.configure(text=str(balance_calculator(income_manager, expense_manager)) + f" {new_currency}")
    
    hello_label = create_hello_label(window, window_width, window_height, user_name)
    manager_label = create_manager_label(window, window_width, window_height)
    income_frame = create_frame(window, window_width, window_height, "#8AC926")
    expense_frame = create_frame(window, window_width, window_height, "#FF595E")
    balance_frame = create_frame(window, window_width, window_height, "#FFCA3A")

    income_frame.place(relx = 0.48, rely = 0.22, anchor = "center")
    expense_frame.place(relx = 0.68, rely = 0.22, anchor = "center")
    balance_frame.place(relx = 0.88, rely = 0.22, anchor = "center")

    income_label = ctk.CTkLabel(income_frame, 
                                text="Total Income",
                                text_color = "#FFF",
                                font = ("Bahnschrift", 16))
    income_label.place(relx = 0.5, rely = 0.9, anchor = "center")

    expense_label = ctk.CTkLabel(expense_frame, 
                                text="Total Expense",
                                text_color = "#FFF",
                                font = ("Bahnschrift", 16))
    expense_label.place(relx = 0.5, rely = 0.9, anchor = "center")

    balance_label = ctk.CTkLabel(balance_frame, 
                                text="Total Balance",
                                text_color = "#FFF",
                                font = ("Bahnschrift", 16))
    balance_label.place(relx = 0.5, rely = 0.9, anchor = "center")

    amount_income_label = ctk.CTkLabel(income_frame, 
                                    text=str(income_calculator(income_manager, expense_manager)) + f" {currency}",
                                    text_color = "#FFF",
                                    font = ("Bahnschrift", 28))
    amount_income_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    amount_expense_label = ctk.CTkLabel(expense_frame, 
                                    text=str(expense_calculator(income_manager, expense_manager)) + f" {currency}",
                                    text_color = "#FFF",
                                    font = ("Bahnschrift", 28))
    amount_expense_label.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    amount_balance_label = ctk.CTkLabel(balance_frame, 
                                    text=str(balance_calculator(income_manager, expense_manager)) + f" {currency}",
                                    text_color = "#FFF",
                                    font = ("Bahnschrift", 28))
    amount_balance_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    window.update()

    def sort_transactions(transactions):
        def parse_date(transaction):
            try:
                date_str = transaction[0][1]
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError as e:
                print(f"Error parsing date '{date_str}' for transaction: {transaction} - {e}")
                return datetime.min

        return sorted(transactions, key=parse_date, reverse=True)

    monthly_incomes = [transaction for transaction in income_manager.read_transactions()]
    monthly_expenses = [transaction for transaction in expense_manager.read_transactions()]

    combined_transactions = [(t, "income") for t in monthly_incomes] + [(t, "expense") for t in monthly_expenses]
    sorted_transactions = sort_transactions(combined_transactions)

    table_frame = ctk.CTkScrollableFrame(window, width=500, height=70, fg_color="lightgrey")
    table_frame.place(relx=0.68, rely=0.7, anchor="center")
    create_table(table_frame, sorted_transactions)
    
    update_table()
    update_labels()

    def open_transaction_window():
        create_transaction_window(window, income_manager, expense_manager, update_table, update_labels, income_categories, expense_categories, window_width, window_height)
    
    def open_ask_summary_window():
        asksummary = ctk.CTkToplevel(window)
        asksummary.title("Monthly summary")
        asksummary.transient(window)
        asksummary.protocol("WM_DELETE_WINDOW", asksummary.withdraw)
        asksummary.withdraw()
        asksummary.configure(bg="#FFFFFF")
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        asksummary_width = int(screen_width * 0.2)
        asksummary_height = int(screen_height * 0.12)
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        asksummary.geometry(f"{asksummary_width}x{asksummary_height}+{int(x)}+{int(y)}")
        asksummary.resizable(False, False)

        asksummary.columnconfigure((0,1), weight = 1, uniform = "a")
        asksummary.rowconfigure((0,1), weight = 2, uniform = "a")
        asksummary.rowconfigure(2, weight = 3, uniform = "a")

        yearentry_label = ctk.CTkLabel(asksummary, 
                        text="Enter the year",
                        text_color = "#1E1E1E",
                        font = ("Bahnschrift", 17))
        yearentry_label.grid(row = 0, column = 0, sticky = "nsew")

        year2_entry = ctk.CTkEntry(asksummary,
                                    corner_radius = 5,
                                    fg_color = "lightgrey",
                                    text_color = "black",
                                    font = ("Bahnschrift", 15),
                                    selectborderwidth = 0
                                    )
        year2_entry.grid(row = 0, column = 1, sticky = "we", padx = 10)

        monthentry_label = ctk.CTkLabel(asksummary, 
                        text="Enter the month",
                        text_color = "#1E1E1E",
                        font = ("Bahnschrift", 17))
        monthentry_label.grid(row = 1, column = 0, sticky = "nsew")

        month2_entry = ctk.CTkEntry(asksummary,
                                    corner_radius = 5,
                                    fg_color = "lightgrey",
                                    text_color = "black",
                                    font = ("Bahnschrift", 15),
                                    selectborderwidth = 0
                                    )
        month2_entry.grid(row = 1, column = 1, sticky = "we", padx = 10)

        def submit_date():
            try:
                year = int(year2_entry.get())
                month = int(month2_entry.get())
                if not (1 <= month <= 12):
                    raise ValueError("Month must be between 1 and 12.")
                _, last_day = calendar.monthrange(year, month)
                end_date = "{}-{:02d}-{}".format(year, month, last_day)
                start_date = "{}-{:02d}-01".format(year, month)

                summarymonthly_incomes = [transaction for transaction in income_manager.read_transactions() if start_date <= transaction[1] <= end_date]
                summarymonthly_expenses = [transaction for transaction in expense_manager.read_transactions() if start_date <= transaction[1] <= end_date]

                start_balance = balance_calculator(income_manager, expense_manager, start_date)
                end_balance = balance_calculator(income_manager, expense_manager, end_date)

                original_date_str = f"{year}-{month}"
                date_obj = datetime.strptime(original_date_str, "%Y-%m")
                new_date_str = date_obj.strftime("%B %Y")

                summarylabel_frame = ctk.CTkFrame(summarywindow, 
                            border_width = 10,
                            border_color = "#1982C4",
                            fg_color = "#1982C4")
                summarylabel_frame.grid(row = 0, column = 0, columnspan = 4, sticky = "nsew", padx = 30, pady = 5)

                summary_label = ctk.CTkLabel(summarylabel_frame, 
                        text=f"Monthly Summary for {new_date_str}",
                        text_color = "#FFFFFF",
                        font = ("Bahnschrift", 25))
                summary_label.place(relx = 0.5, rely = 0.5, anchor = "center")

                aincometotal_label = ctk.CTkLabel(summarywindow, 
                            text=f"{sum(float(record[0]) for record in monthly_incomes)}",
                            text_color = "#1E1E1E",
                            font = ("Bahnschrift", 18))
                aincometotal_label.grid(row = 1, column = 1, sticky = "nsew")

                aexpensetotal_label = ctk.CTkLabel(summarywindow, 
                            text=f"{sum(float(record[0]) for record in monthly_expenses)}",
                            text_color = "#1E1E1E",
                            font = ("Bahnschrift", 18))
                aexpensetotal_label.grid(row = 2, column = 1, sticky = "nsew")

                abalancestart_label = ctk.CTkLabel(summarywindow, 
                            text=f"{start_balance}",
                            text_color = "#1E1E1E",
                            font = ("Bahnschrift", 18))
                abalancestart_label.grid(row = 1, column = 3, sticky = "nsew")

                abalanceend_label = ctk.CTkLabel(summarywindow, 
                            text=f"{end_balance}",
                            text_color = "#1E1E1E",
                            font = ("Bahnschrift", 18))
                abalanceend_label.grid(row = 2, column = 3, sticky = "nsew")

                anetchange_label = ctk.CTkLabel(summarywindow, 
                            text=f"{end_balance - start_balance}",
                            text_color = "#1E1E1E",
                            font = ("Bahnschrift", 20))
                anetchange_label.grid(row = 3, column = 2, columnspan = 2, sticky = "w", padx = 20)

                summarycombined_transactions = [(t, "income") for t in summarymonthly_incomes] + [(t, "expense") for t in summarymonthly_expenses]
                summarysorted_transactions = sort_transactions(summarycombined_transactions)

                summarytable_frame = ctk.CTkScrollableFrame(summarywindow, fg_color="lightgrey")
                summarytable_frame.grid(row = 5, column = 0, columnspan = 4, sticky = "nsew", padx = 15, pady=15)
                create_table(summarytable_frame, summarysorted_transactions)

                asksummary.withdraw()
                summarywindow.deiconify()

            except ValueError as e:
                CTkMessagebox(title="Input Error", message=str(e), icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Unexpected Error", message=str(e), icon="cancel")

        asksubmit = ctk.CTkButton(asksummary,
                                    text = "View the summary",
                                    width = int(window_width / 3.14),
                                    height = int(window_height / 11.25),
                                    corner_radius = 5,
                                    fg_color = "#1982C4",
                                    hover_color = "#1982C4",
                                    text_color = "white",
                                    font = ("Bahnschrift", 18),
                                    command = submit_date)
        asksubmit.grid(row = 2, column = 0, columnspan = 2) 

        asksummary.deiconify()

    addtransaction_button = ctk.CTkButton(window,
                                          text = "Add transaction",
                                          width = int(window_width / 3.14),
                                          height = int(window_height / 11.25),
                                          corner_radius = 5,
                                          fg_color = "#1982C4",
                                          hover_color = "#1982C4",
                                          text_color = "white",
                                          font = ("Bahnschrift", 20),
                                          command=open_transaction_window
                                          )
    addtransaction_button.place(relx = 0.18, rely = 0.42, anchor = "center")

    showsummary_button = ctk.CTkButton(window,
                                          text = "Show summary for month",
                                          width = int(window_width / 3.14),
                                          height = int(window_height / 11.25),
                                          corner_radius = 5,
                                          fg_color = "#1982C4",
                                          hover_color = "#1982C4",
                                          text_color = "white",
                                          font = ("Bahnschrift", 20),
                                          command = open_ask_summary_window
                                          )
    showsummary_button.place(relx = 0.18, rely = 0.55, anchor = "center")

    changename_button = ctk.CTkButton(window,
                                          text = "Change my name",
                                          width = int(window_width / 3.14),
                                          height = int(window_height / 11.25),
                                          corner_radius = 5,
                                          fg_color = "#6A4C93",
                                          hover_color = "#6A4C93",
                                          text_color = "white",
                                          font = ("Bahnschrift", 20),
                                          command=open_name_update_dialog)
    changename_button.place(relx = 0.18, rely = 0.68, anchor = "center")

    changecurrency_button = ctk.CTkButton(window,
                                          text = "Change currency",
                                          width = int(window_width / 3.14),
                                          height = int(window_height / 11.25),
                                          corner_radius = 5,
                                          fg_color = "#6A4C93",
                                          hover_color = "#6A4C93",
                                          text_color = "white",
                                          font = ("Bahnschrift", 20),
                                          command=open_currency_update_dialog)
    changecurrency_button.place(relx = 0.18, rely = 0.81, anchor = "center")

    summarywindow = ctk.CTkToplevel(window)
    summarywindow.title("Montly Summary")
    summarywindow.transient(window)
    summarywindow.protocol("WM_DELETE_WINDOW", summarywindow.withdraw)
    summarywindow.withdraw()
    summarywindow.configure(bg="#FFFFFF")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    summarywindow_width = int(screen_width * 0.4)
    summarywindow_height = int(screen_height * 0.6)
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    summarywindow.geometry(f"{summarywindow_width}x{summarywindow_height}+{int(x)}+{int(y)}")
    summarywindow.resizable(False, False)

    summarywindow.columnconfigure((1,3), weight = 2, uniform = "a")
    summarywindow.columnconfigure((0,2), weight = 3, uniform = "a")
    summarywindow.rowconfigure((0,1,2,3,4), weight = 1, uniform = "a")
    summarywindow.rowconfigure(5, weight = 5, uniform = "a")

    incomesummary_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#8AC926",
                         fg_color = "#8AC926")
    incomesummary_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 5, pady = 5)

    incometotal_label = ctk.CTkLabel(incomesummary_frame, 
                       text="Total Income",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 18))
    incometotal_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    expensesummary_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#FF595E",
                         fg_color = "#FF595E")
    expensesummary_frame.grid(row = 2, column = 0, sticky = "nsew", padx = 5, pady = 5)

    expensetotal_label = ctk.CTkLabel(expensesummary_frame, 
                       text="Total Expense",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 18))
    expensetotal_label.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    balancestart_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#FFCA3A",
                         fg_color = "#FFCA3A")
    balancestart_frame.grid(row = 1, column = 2, sticky = "nsew", pady = 5)

    balancestart_label = ctk.CTkLabel(balancestart_frame, 
                       text="Balance at the start\nof the month",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 16))
    balancestart_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    balanceend_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#FFCA3A",
                         fg_color = "#FFCA3A")
    balanceend_frame.grid(row = 2, column = 2, sticky = "nsew", pady = 5)

    balanceend_label = ctk.CTkLabel(balanceend_frame, 
                       text="Balance at the end\nof the month",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 16))
    balanceend_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    netchange_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#6A4C93",
                         fg_color = "#6A4C93")
    netchange_frame.grid(row = 3, column = 0, columnspan = 2, sticky = "e", pady = 5, padx = 5)

    netchange_label = ctk.CTkLabel(netchange_frame, 
                       text="Net Change",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 20))
    netchange_label.place(relx = 0.5, rely = 0.5, anchor = "center")

    incomesexpenseslabel_frame = ctk.CTkFrame(summarywindow, 
                         border_width = 10,
                         border_color = "#1982C4",
                         fg_color = "#1982C4")
    incomesexpenseslabel_frame.grid(row = 4, column = 0, columnspan = 4, sticky = "sew", padx = 30, pady = 5)

    incomesexpenses_label = ctk.CTkLabel(incomesexpenseslabel_frame, 
                       text="Incomes and Expenses",
                       text_color = "#FFFFFF",
                       font = ("Bahnschrift", 25))
    incomesexpenses_label.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    window.mainloop()

if __name__ == '__main__':
    main()