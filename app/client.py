from psycopg2.errors import UniqueViolation

class CLI:
    def __init__(self, manager):
        self.manager = manager

    def user(self):
        while True:
            print("Login / register / exit")
            a = input(" : ").strip().lower()
            if a == "register":
                print("-"*5 + "registration")
                username = input("Enter a username : ")
                password = input("Enter a password : ")
                try:
                    self.manager.add_user(username, password)
                    print("User registered successfully")
                except ValueError as e:
                    print(f"!!! {e}")
                continue
            elif a == "login":
                print("login" + "-"*5)
                username = input("Enter a username : ")
                password = input("Enter a password : ")
                try:
                    user_id = self.manager.login(username, password)
                    if user_id is not None:
                        print("< - Login successful - >")
                        return user_id
                    else:
                        continue
                except ValueError:
                    print("!!! Wrong username or password")
            elif a == "exit":
                return None
            else:
                print("!!! Unknown command")

    def run(self):
        while True:
            print("Commands: add / transactions / exit")
            command = input("> ").strip().lower()
            if command == "add":
                print("Enter transaction details (type, amount, category, description):")
                transaction_type = input("Type (income/expense): ")
                amount = input("Amount : ")
                category = input("Category : ")
                description = input("Description (enter to skip) : ")
                try:
                    self.manager.add_transaction(transaction_type, amount, category, description)
                    print("Saved")
                except ValueError as e:
                    print(f"!!! {e}")

            elif command == "transactions":
                print("Options: All / Type / Category / Delete /\n Statistic / Exit")
                choice = input("> ").strip().lower()
                if choice == "category":
                    print(f"Available categories:\n{", ".join(self.manager.VALID_CATEGORIES)}")
                    category = input("> ").strip().lower()
                    transactions = self.manager.get_transactions("category", category)
                    if not transactions:
                        print("No transactions found in this category")
                    else:
                        for i, line in enumerate(transactions, start=1):
                            print(f"{i}. [{line[1]}] — {line[3]}: {line[2]} {line[4]} ({line[5]})")
                elif choice == "type":
                    print("Available types:\nincome / expense")
                    type_of = input("> ").strip().lower()
                    transactions = self.manager.get_transactions("type_of", type_of)
                    if transactions:
                        for i, line in enumerate(transactions, start=1):
                            print(f"{i}. [{line[1]}] — {line[3]}: {line[2]} {line[4]} ({line[5]})")
                    else:
                        print("No transactions found for this type")
                elif choice == "all":
                    transactions = self.manager.get_all_transactions()
                    if transactions:
                        for i, line in enumerate(transactions, start=1):
                            print(f"{i}. [{line[1]}] — {line[3]}: {line[2]} {line[4]} ({line[5]})")
                    else:
                        print("No transactions found")
                elif choice == "delete":
                    transactions = self.manager.get_all_transactions()
                    print("Select a transaction number to delete")
                    if transactions:
                        for i, line in enumerate(transactions, start=1):
                            print(f"{i}. [{line[1]}] {line[3]}: {line[2]}")
                        number = input("Enter transaction number : ")
                        try:
                            self.manager.delete_transaction(number)
                            print(f'Transaction #{number} has been deleted')
                        except ValueError as e:
                            print(f"!!! {e}")
                    else:
                        print("No transactions available to delete")
                elif choice == "statistic":
                    word = input("Filter statistics by (type / category) : ")
                    try:
                        if word in ("type", "category"):
                            transactions = self.manager.statistic(word)
                            if transactions:
                                for line in transactions:
                                    print(f"{line[0]} : {line[1]}")
                            else:
                                print("No data available for statistics")
                        else:
                            print("!!! Invalid option. Please choose 'type' or 'category'")
                    except ValueError:
                        print("No transactions found")
                elif choice == "exit":
                    pass
                else:
                    print("Unknown command")
                    continue
            elif command == "exit":
                break
            else:
                print("Unknown command")