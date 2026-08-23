def add_fruit():

    show_stock()

    item = input("enter the fruit name or id to add: ").strip()

    if item.isdigit():

        item = int(item)

        if 1 <= item <= len(fruits):

            fruit = list(fruits.keys())[item - 1]

            quantity = input(f"Enter the quantity of {fruit} to add: ")

            if not quantity.isdigit() or int(quantity) <= 0:
                print("Invalid quantity. Please enter a positive integer.")
                return

            quantity = int(quantity)
            fruits[fruit] += quantity

        else:
            print("Invalid id.")
            return

    else:

        fruit = item.lower()

        amount = input(f"Enter the quantity of {fruit} to add: ")

        if not amount.isdigit() or int(amount) <= 0:
            print("Invalid quantity. Please enter a positive integer.")
            return

        amount = int(amount)

        if fruit in fruits:
            fruits[fruit] += amount

        else:
            fruits[fruit] = amount


def remove_fruit():

    show_stock()

    item = input("enter the fruit name or id to remove: ").strip()

    if item.isdigit():

        item = int(item)

        if 1 <= item <= len(fruits):

            fruit = list(fruits.keys())[item - 1]

            quantity = input(f"Enter the quantity of {fruit} to remove: ")

            if not quantity.isdigit() or int(quantity) <= 0:
                print("Invalid quantity. Please enter a positive integer.")
                return

            quantity = int(quantity)

            if quantity > fruits[fruit]:
                print("Invalid quantity. Please enter a positive integer less than or equal to the available stock.")
                return

            fruits[fruit] -= quantity

        else:
            print("Invalid id.")
            return

    else:

        fruit = item.lower()

        if fruit in fruits:

            amount = input(f"Enter the quantity of {fruit} to remove: ")

            if not amount.isdigit() or int(amount) <= 0:
                print("Invalid quantity. Please enter a positive integer less than or equal to the available stock.")
                return

            amount = int(amount)

            if amount > fruits[fruit]:
                print("Invalid quantity. Please enter a positive integer less than or equal to the available stock.")
                return

            fruits[fruit] -= amount

        else:
            print(f"{fruit} is not in stock.")


def show_stock():

    for id, (fruit, quantity) in enumerate(fruits.items(), start=1):
        print(f"{id}. {fruit} - {quantity}")


def save_stock():

    with open("stock.txt", "w") as f:

        for fruit, quantity in fruits.items():
            f.write(f"{fruit},{quantity}\n")


fruits = {}

try:
    with open("stock.txt", "r") as f:

        for line in f:

            fruit, quantity = line.strip().split(",")

            fruits[fruit.lower()] = int(quantity)

except FileNotFoundError:

    print("Stock file not found. Starting with an empty stock.")

except ValueError:

    print("Error reading stock file. Please check the file format.")



while True:

    print("----------------options----------------")
    print("1. Add fruit")
    print("2. Remove fruit")
    print("3. Show stock")
    print("4. Exit")

    x = input("Enter your choice: ")

    match x:

        case "1":
            add_fruit()
            save_stock()

        case "2":
            remove_fruit()
            save_stock()

        case "3":
            show_stock()

        case "4":
            save_stock()
            break

        case _:
            print("Invalid choice. Please try again.")