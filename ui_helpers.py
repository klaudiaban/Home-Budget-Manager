import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from CTkTable import CTkTable
import csv
import calendar

def initialize_main_window():
    window = ctk.CTk()
    window.title("Budget Manager")
    window.configure(bg="#FFFFFF")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width * 0.6)
    window_height = int(screen_height * 0.5)

    window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
    window.resizable(False, False)
    return window, window_width, window_height

def create_hello_label(window, window_width, window_height, user_name):
    hello_label = ctk.CTkLabel(window, 
                        text=f"Hello, {user_name}!",
                       text_color = "#1E1E1E",
                       width = int(window_width / 3.3),
                       height = int(window_height / 9.375),
                       font = ("Bahnschrift", 36))
    hello_label.place(relx = 0.18, rely = 0.15, anchor = "center")
    return hello_label

def create_manager_label(window, window_width, window_height):
    manager_label = ctk.CTkLabel(window, 
                       text="I’m your Budget Manager,\nwhat can I do for you?",
                       text_color = "#1E1E1E",
                       width = int(window_width / 3.3),
                       height = int(window_height / 9),
                       font = ("Bahnschrift", 20))
    manager_label.place(relx = 0.18, rely = 0.26, anchor = "center")
    return manager_label

def create_frame(window, window_width, window_height, color):
    frame = ctk.CTkFrame(window, 
                         width=int(window_width / 5.76), 
                         height=int(window_height / 3),
                         border_width = 10,
                         border_color = color,
                         fg_color = color)
    return frame

def create_table(frame, transactions):
    values = [("Amount", "Date", "Category", "Description", "Type")]

    for transaction, t_type in transactions:
        color_indicator = "income" if t_type == "income" else "expense"
        row = list(transaction) + [color_indicator]
        values.append(row)

    table = CTkTable(frame, row=len(values), column=5, values=values, hover_color="darkgrey", header_color="white", wraplength=175)
    table.pack(expand=True, fill="both", padx=5, pady=5)

def create_name_update_dialog(window, submit_action, window_width, window_height):
    ndialog = ctk.CTkToplevel(window)
    ndialog.title("Update name")
    ndialog.geometry("300x150")
    ndialog.resizable(False, False)
    ndialog.columnconfigure(0, weight = 1, uniform = "a")
    ndialog.rowconfigure((0,1), weight = 2, uniform = 'a')
    ndialog.rowconfigure((2), weight = 3, uniform = 'a')

    nlabel = ctk.CTkLabel(ndialog, text="Update your name",
                            text_color = "#1E1E1E",
                            width = int(window_width / 3.3),
                            height = int(window_height / 9),
                            font = ("Bahnschrift", 20))
    nlabel.grid(row = 0, column = 0, sticky = "nsew")

    nentry = ctk.CTkEntry(ndialog, corner_radius = 5,
                            fg_color = "lightgrey",
                            text_color = "black",
                            font = ("Bahnschrift", 15),
                            selectborderwidth = 0)
    nentry.grid(row = 1, column = 0)

    def on_nsubmit():
        submit_action(nentry.get())
        ndialog.destroy()

    nsubmitbutton = ctk.CTkButton(ndialog,
                            text = "Submit information",
                            width = int(window_width / 3.14),
                            height = int(window_height / 11.25),
                            corner_radius = 5,
                            fg_color = "#6A4C93",
                            hover_color = "#6A4C93",
                            text_color = "white",
                            font = ("Bahnschrift", 20),
                            command = on_nsubmit)
    nsubmitbutton.grid(row = 2, column = 0) 

    ndialog.transient(window)  
    ndialog.grab_set() 
    ndialog.wait_window() 

def create_currency_update_dialog(window, submit_action, window_width, window_height):
    cdialog = ctk.CTkToplevel(window)
    cdialog.title("Update currency")
    cdialog.geometry("300x150")
    cdialog.resizable(False, False)
    cdialog.columnconfigure(0, weight = 1, uniform = "a")
    cdialog.rowconfigure((0,1), weight = 2, uniform = 'a')
    cdialog.rowconfigure((2), weight = 3, uniform = 'a')

    clabel = ctk.CTkLabel(cdialog, text="Update currency",
                            text_color = "#1E1E1E",
                            width = int(window_width / 3.3),
                            height = int(window_height / 9),
                            font = ("Bahnschrift", 20))
    clabel.grid(row = 0, column = 0, sticky = "nsew")

    cmenu = ctk.CTkOptionMenu(cdialog, values=["zl", "$", "€"],
                                        font = ("Bahnschrift", 15),
                                        corner_radius = 5,
                                        fg_color = "lightgrey",
                                        button_color = "darkgrey",
                                        button_hover_color = "grey",
                                        dropdown_fg_color = 'lightgrey',
                                        dropdown_text_color = "black",
                                        text_color = "black",
                                        dropdown_font = ("Bahnschrift", 15))
    cmenu.grid(row = 1, column = 0)

    def on_csubmit():
        submit_action(cmenu.get())
        cdialog.destroy()

    csubmitbutton = ctk.CTkButton(cdialog,
                            text = "Submit information",
                            width = int(window_width / 3.14),
                            height = int(window_height / 11.25),
                            corner_radius = 5,
                            fg_color = "#6A4C93",
                            hover_color = "#6A4C93",
                            text_color = "white",
                            font = ("Bahnschrift", 20),
                            command = on_csubmit)
    csubmitbutton.grid(row = 2, column = 0) 

    cdialog.transient(window)  
    cdialog.grab_set() 
    cdialog.wait_window() 

def create_transaction_window(window, income_manager, expense_manager, update_table, update_labels, income_categories, expense_categories, window_width, window_height):
    transactionwindow = ctk.CTkToplevel(window)
    transactionwindow.title("Add Transaction")
    transactionwindow.transient(window)
    transactionwindow.protocol("WM_DELETE_WINDOW", transactionwindow.withdraw)
    transactionwindow.withdraw()
    transactionwindow.configure(bg="#FFFFFF")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    transactionwindow_width = int(screen_width * 0.25)
    transactionwindow_height = int(screen_height * 0.4)
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    transactionwindow.geometry(f"{transactionwindow_width}x{transactionwindow_height}+{int(x)}+{int(y)}")
    transactionwindow.resizable(False, False)

    transactionwindow.columnconfigure(0, weight = 3, uniform = "a")
    transactionwindow.columnconfigure((1,2,3), weight = 1, uniform = "a")
    transactionwindow.rowconfigure((0,1,2,3,4,5), weight = 1, uniform = "a")

    optionmenu_label = ctk.CTkLabel(transactionwindow, 
                       text="Choose the type \nof transaction",
                       text_color = "#1E1E1E",
                       font = ("Bahnschrift", 17))
    optionmenu_label.grid(row = 0, column = 0, sticky = "nsew")

    def update_category_menu(selected_option):
        categories = income_categories if selected_option == "Income" else expense_categories
        categorymenu.configure(values=categories)
        categorymenu.set(categories[0])

    optionmenu = ctk.CTkOptionMenu(transactionwindow, values=["Income", "Expense"],
                                            font = ("Bahnschrift", 15),
                                            corner_radius = 5,
                                            fg_color = "lightgrey",
                                            button_color = "darkgrey",
                                            button_hover_color = "grey",
                                            dropdown_fg_color = 'lightgrey',
                                            dropdown_text_color = "black",
                                            text_color = "black",
                                            dropdown_font = ("Bahnschrift", 15),
                                            command = update_category_menu)
    optionmenu.set("Expense")
    optionmenu.grid(row = 0, column = 1, columnspan = 3, sticky = "we", padx = 10)

    amountentry_label = ctk.CTkLabel(transactionwindow, 
                       text="Enter the amount \nof transaction",
                       text_color = "#1E1E1E",
                       font = ("Bahnschrift", 17))
    amountentry_label.grid(row = 1, column = 0, sticky = "nsew")

    amount_entry = ctk.CTkEntry(transactionwindow,
                                corner_radius = 5,
                                fg_color = "lightgrey",
                                text_color = "black",
                                font = ("Bahnschrift", 15),
                                selectborderwidth = 0
                                )
    amount_entry.grid(row = 1, column = 1, columnspan = 3, sticky = "we", padx = 10)

    categorymenu_label = ctk.CTkLabel(transactionwindow, 
                       text="Choose the category \nof transaction",
                       text_color = "#1E1E1E",
                       width = int(window_width / 3.36),
                       height = int(window_height / 22.5),
                       font = ("Bahnschrift", 16))
    categorymenu_label.grid(row = 2, column = 0, sticky = "nsew")

    categorymenu = ctk.CTkOptionMenu(transactionwindow, values=expense_categories,
                                            font = ("Bahnschrift", 15),
                                            corner_radius = 5,
                                            fg_color = "lightgrey",
                                            button_color = "darkgrey",
                                            button_hover_color = "grey",
                                            dropdown_fg_color = 'lightgrey',
                                            dropdown_text_color = "black",
                                            text_color = "black",
                                            dropdown_font = ("Bahnschrift", 15),)
    categorymenu.set(expense_categories[0])
    categorymenu.grid(row = 2, column = 1, columnspan = 3, sticky = "we", padx = 10)

    descriptionentry_label = ctk.CTkLabel(transactionwindow, 
                       text="Enter the description",
                       text_color = "#1E1E1E",
                       font = ("Bahnschrift", 16))
    descriptionentry_label.grid(row = 3, column = 0, sticky = "nsew")

    description_entry = ctk.CTkEntry(transactionwindow,
                                corner_radius = 5,
                                fg_color = "lightgrey",
                                text_color = "black",
                                font = ("Bahnschrift", 15),
                                selectborderwidth = 0
                                )
    description_entry.grid(row = 3, column = 1, columnspan = 3, sticky = "we", padx = 10)

    dateentry_label = ctk.CTkLabel(transactionwindow, 
                       text="Enter the date",
                       text_color = "#1E1E1E",
                       font = ("Bahnschrift", 17))
    dateentry_label.grid(row = 4, column = 0, sticky = "nsew")
    
    day_entry = ctk.CTkEntry(transactionwindow, placeholder_text="Day", width=50,
                             font = ("Bahnschrift", 15),
                             text_color = "black")
    day_entry.grid(row = 4, column = 1, sticky = 'e')

    month_entry = ctk.CTkEntry(transactionwindow)
    month_entry = ctk.CTkEntry(transactionwindow, placeholder_text="Month", width=50,
                               font = ("Bahnschrift", 15),
                               text_color = "black")
    month_entry.grid(row = 4, column = 2)

    year_entry = ctk.CTkEntry(transactionwindow, placeholder_text="Year", width=50,
                              font = ("Bahnschrift", 15),
                              text_color = "black")
    year_entry.grid(row = 4, column = 3, sticky = 'w')

    def process_transaction():
        try:
            transaction_type = optionmenu.get()
            amount_str = amount_entry.get()
            day_str = day_entry.get()
            month_str = month_entry.get()
            year_str = year_entry.get()
            category = categorymenu.get()
            description = description_entry.get()

            if not (amount_str and day_str and month_str and year_str):
                raise ValueError("All fields must be filled.")

            amount = float(amount_str)
            day = int(day_str)
            month = int(month_str)
            year = int(year_str)

            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            try:
                new_date = datetime(year, month, day)
            except ValueError as e:
                raise ValueError(f"Invalid date: {e}")

            date = new_date.strftime("%Y-%m-%d")
            category = categorymenu.get()
            description = description_entry.get()
            transaction = [amount, date, category, description]

            if transaction_type == "Income":
                income_manager.add_transaction(transaction)
            elif transaction_type == "Expense":
                expense_manager.add_transaction(transaction)
            else:
                raise ValueError("Invalid transaction type.")
            
            update_table()
            update_labels()
            transactionwindow.withdraw()

        except ValueError as e:
            CTkMessagebox(title="Input Error", message=str(e), icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Unexpected Error", message=str(e), icon="cancel")

    submitbutton = ctk.CTkButton(transactionwindow,
                                text = "Submit transaction",
                                width = int(window_width / 3.14),
                                height = int(window_height / 11.25),
                                corner_radius = 5,
                                fg_color = "#1982C4",
                                hover_color = "#1982C4",
                                text_color = "white",
                                font = ("Bahnschrift", 20),
                                command = process_transaction)
    submitbutton.grid(row = 5, column = 0, columnspan = 4) 

    transactionwindow.deiconify()

def create_ask_summary_window(window, summarywindow, window_width, window_height, income_manager, expense_manager, BalanceCalculator, sort_transactions, update_labels):
    def update_summary(year, month):
        _, last_day = calendar.monthrange(year, month)
        end_date = "{}-{:02d}-{}".format(year, month, last_day)
        start_date = "{}-{:02d}-01".format(year, month)

        summarymonthly_incomes = [transaction for transaction in income_manager.read_transactions() if start_date <= transaction[1] <= end_date]
        summarymonthly_expenses = [transaction for transaction in expense_manager.read_transactions() if start_date <= transaction[1] <= end_date]

        start_balance = BalanceCalculator.calculate_balance(income_manager, expense_manager, start_date)
        end_balance = BalanceCalculator.calculate_balance(income_manager, expense_manager, end_date)

        original_date_str = f"{year}-{month}"
        date_obj = datetime.strptime(original_date_str, "%Y-%m")
        new_date_str = date_obj.strftime("%B %Y")

        summary_label.configure(text=f"Monthly Summary for {new_date_str}")
        aincometotal_label.configure(text=f"{sum(float(record[0]) for record in summarymonthly_incomes)}")
        aexpensetotal_label.configure(text=f"{sum(float(record[0]) for record in summarymonthly_expenses)}")
        abalancestart_label.configure(text=f"{start_balance}")
        abalanceend_label.configure(text=f"{end_balance}")
        anetchange_label.configure(text=f"{end_balance - start_balance}")

        summarycombined_transactions = [(t, "income") for t in summarymonthly_incomes] + [(t, "expense") for t in summarymonthly_expenses]
        summarysorted_transactions = sort_transactions(summarycombined_transactions)

        for widget in summarytable_frame.winfo_children():
            widget.destroy()
        create_table(summarytable_frame, summarysorted_transactions)

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
                    text=f"{sum(float(record[0]) for record in summarymonthly_incomes)}",
                    text_color = "#1E1E1E",
                    font = ("Bahnschrift", 18))
        aincometotal_label.grid(row = 1, column = 1, sticky = "nsew")

        aexpensetotal_label = ctk.CTkLabel(summarywindow, 
                    text=f"{sum(float(record[0]) for record in summarymonthly_incomes)}",
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
                                selectborderwidth = 0)
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
                                selectborderwidth = 0)
    month2_entry.grid(row = 1, column = 1, sticky = "we", padx = 10)

    def submit_date():
        try:
            year = int(year2_entry.get())
            month = int(month2_entry.get())
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12.")
            
            update_summary(year, month)
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

def ask_user_info(window, user_info_file, window_width, window_height):
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

    user_name, currency = read_user_info()
    if user_name is not None and currency is not None:
        return user_name, currency
                
    info_dialog = ctk.CTkToplevel(window)
    info_dialog.title("User Information")
    info_dialog_width = int(window_width * 0.4)
    info_dialog_height = int(window_height * 0.75)
    info_dialog.geometry(f"{info_dialog_width}x{info_dialog_height}")
    info_dialog.transient(window)
    info_dialog.resizable(False, False)
    info_dialog.grab_set()

    info_dialog.columnconfigure(0, weight = 1, uniform = "a")
    info_dialog.rowconfigure((1,2,3,4), weight = 2, uniform = "a")
    info_dialog.rowconfigure((0,5), weight = 3, uniform = "a")

    hi_label = ctk.CTkLabel(info_dialog, text="Hello! Give me some\ninformation about you :)",
                            text_color = "#1E1E1E",
                            width = int(window_width / 3.3),
                            height = int(window_height / 9),
                            font = ("Bahnschrift", 22))
    hi_label.grid(row = 0, column = 0, sticky = "nsew")
    name_label = ctk.CTkLabel(info_dialog, text="First question:\nWhat's your name?",
                            text_color = "#1E1E1E",
                            width = int(window_width / 3.3),
                            height = int(window_height / 9),
                            font = ("Bahnschrift", 20))
    name_label.grid(row = 1, column = 0, sticky = "nsew")
    name_entry = ctk.CTkEntry(info_dialog, corner_radius = 5,
                            fg_color = "lightgrey",
                            text_color = "black",
                            font = ("Bahnschrift", 15),
                            selectborderwidth = 0)
    name_entry.grid(row = 2, column = 0)

    currency_label = ctk.CTkLabel(info_dialog, text="Second question:\nWhat type of currency do you use?",
                            text_color = "#1E1E1E",
                            width = int(window_width / 3.3),
                            height = int(window_height / 9),
                            font = ("Bahnschrift", 20))
    currency_label.grid(row = 3, column = 0, sticky = "nsew")
    currencymenu = ctk.CTkOptionMenu(info_dialog, values=["zl", "$", "€"],
                                        font = ("Bahnschrift", 15),
                                        corner_radius = 5,
                                        fg_color = "lightgrey",
                                        button_color = "darkgrey",
                                        button_hover_color = "grey",
                                        dropdown_fg_color = 'lightgrey',
                                        dropdown_text_color = "black",
                                        text_color = "black",
                                        dropdown_font = ("Bahnschrift", 15))
    currencymenu.grid(row = 4, column = 0)

    def submit_info():
        nonlocal user_name, currency
        try:
            user_name = name_entry.get()
            currency = currencymenu.get()
            if not user_name:
                raise ValueError("Name field must be filled.")
            info_dialog.destroy()
        except ValueError as e:
            CTkMessagebox(title="Input Error", message=str(e), icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Unexpected Error", message=str(e), icon="cancel")

    submitinfobutton = ctk.CTkButton(info_dialog,
                            text = "Submit information",
                            width = int(window_width / 3.14),
                            height = int(window_height / 11.25),
                            corner_radius = 5,
                            fg_color = "#1982C4",
                            hover_color = "#1982C4",
                            text_color = "white",
                            font = ("Bahnschrift", 20),
                            command = submit_info)
    submitinfobutton.grid(row = 5, column = 0) 

    info_dialog.wait_window()

    stored_name, stored_currency = read_user_info()
    if stored_name is not None and stored_currency is not None:
        return stored_name, stored_currency

    if user_name and currency:
        write_user_info(user_name, currency)

    return user_name, currency


