class Food:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Customer:
    def __init__(self, name):
        self.name = name

    def place_order(self, food_items):
        total_price = sum(food.price * quantity for food, quantity in food_items)
        return total_price

    def rate_order(self, order_id, rating, food_items):
        with open("bills.txt", "a") as file:
            file.write(f"Order ID: {order_id}\n")
            file.write(f"Customer: {self.name}\n")
            file.write("Food Items:\n")
            for food, quantity in food_items:
                file.write(f"{food.name}:  {food.price} x {quantity}\n")
            file.write(f"Total Price:  {self.place_order(food_items)}\n")
            file.write(f"Rating: {rating}\n")
            file.write("-------------------\n")


class Admin:
    def __init__(self):
        self.menu_file = "menu.txt"
        self.bill_file = "bills.txt"

    def add_food_item(self, food_item):
        with open(self.menu_file, "a") as file:
            file.write(f"{food_item.name},{food_item.price}\n")
        print(f"Food item '{food_item.name}' added to the menu.")

    def delete_food_item(self, food_name):
        lines = []
        with open(self.menu_file, "r") as file:
            for line in file:
                if not line.startswith(food_name):
                    lines.append(line)
        with open(self.menu_file, "w") as file:
            file.writelines(lines)
        print(f"Food item '{food_name}' deleted from the menu.")

    def update_food_price(self, food_name, new_price):
        lines = []
        with open(self.menu_file, "r") as file:
            for line in file:
                if line.startswith(food_name):
                    name, _ = line.strip().split(",")
                    line = f"{name},{new_price}\n"
                lines.append(line)
        with open(self.menu_file, "w") as file:
            file.writelines(lines)
        print(f"Price for food item '{food_name}' updated to  {new_price}")

    def view_menu(self):
        print("Menu:")
        print("------------------------------------")
        print("|   Number   |    Item     |  Price(Rs)  |")
        print("------------------------------------")
        with open(self.menu_file, "r") as file:
            menu_items = file.readlines()
            for number, item in enumerate(menu_items, start=1):
                name, price = item.strip().split(",")
                print(f"|{str(number).center(12)}| {name.ljust(12)} |   {price.rjust(8)}  |")
        print("------------------------------------")

    def view_previous_bills(self):
        print("Previous Bills:")
        with open(self.bill_file, "r") as file:
            print(file.read())


# Creating admin instance
admin = Admin()
admin_password = "6363"
max_attempts = 3
attempt_count = 0

while True:
    print("\nWelcome to the Food Ordering System!")
    print("1. Customer Section")
    print("2. Admin Section")
    print("3. Exit")
    choice = input("Please select a section (1/2/3): ")

    if choice == "1":
        print("\n--- Customer Section ---")
        customer_name = input("Enter your name: ")
        customer = Customer(customer_name)

        print("Available Menu:")
        admin.view_menu()

        food_items = []
        while True:
            food_number = input("\nEnter the number of the food item (or 'exit' to go back): ")
            if food_number == "exit":
                break

            with open(admin.menu_file, "r") as file:
                menu_items = file.readlines()
                try:
                    food_index = int(food_number) - 1
                    if 0 <= food_index < len(menu_items):
                        name, price = menu_items[food_index].strip().split(",")
                        quantity = int(input("Enter the quantity: "))
                        food_items.append((Food(name, float(price)), quantity))
                    else:
                        print("Invalid food item number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        total_price = customer.place_order(food_items)
        print("\n--- Order Details ---")
        print("Customer: ", customer.name)
        print("-------------------------------------------------")
        print("|     Food Item      |  Quantity  |  Price      |")
        print("-------------------------------------------------")
        for food, quantity in food_items:
            print(f"| {food.name.ljust(18)} | {str(quantity).rjust(10)} |  {str(food.price * quantity).rjust(10)} |")
        print("-------------------------------------------------")
        print("                            |Total Price:  ", total_price)
        print("-------------------------------------------------")
        order_id = len(open(admin.bill_file).readlines()) // 8  # Assuming each order takes 8 lines in the bill file
        rating = input("Please rate your order (1-5 stars): ")
        customer.rate_order(order_id, rating, food_items)

    elif choice == "2":
        print("\n--- Admin Section ---")
        while True:
            admin_password_attempt = input("Enter the admin password: ")
            if admin_password_attempt == admin_password:
                print("\nAccess granted!")
                break

            attempt_count += 1
            if attempt_count >= max_attempts:
                print("\nMax number of attempts reached. Exiting admin section.")
                break

            remaining_attempts = max_attempts - attempt_count
            print(f"Access denied! Please try again. ({remaining_attempts} attempt(s) remaining)")

        if admin_password_attempt == admin_password:
            while True:
                print("\n1. View Menu")
                print("2. Add Food Item")
                print("3. Delete Food Item")
                print("4. Update Food Price")
                print("5. View Previous Bills")
                print("6. Go Back")
                admin_choice = input("Please select an option (1/2/3/4/5/6): ")

                if admin_choice == "1":
                    print("\n--- Menu ---")
                    admin.view_menu()

                elif admin_choice == "2":
                    print("\n--- Add Food Item ---")
                    food_name = input("Enter the name of the food item: ")
                    food_price = input("Enter the price of the food item: ")
                    admin.add_food_item(Food(food_name, float(food_price)))

                elif admin_choice == "3":
                    print("\n--- Delete Food Item ---")
                    food_name = input("Enter the name of the food item to delete: ")
                    admin.delete_food_item(food_name)

                elif admin_choice == "4":
                    print("\n--- Update Food Price ---")
                    food_name = input("Enter the name of the food item to update: ")
                    new_price = input("Enter the new price for the food item: ")
                    admin.update_food_price(food_name, float(new_price))

                elif admin_choice == "5":
                    print("\n--- Previous Bills ---")
                    admin.view_previous_bills()

                elif admin_choice == "6":
                    break

    elif choice == "3":
            print("Thank you for using the Food Ordering System!")
            break

    else:
        print("Invalid choice. Please try again.")



