from product_manager import add_product, delete_product, list_products, update_product_price, apply_discount


def menu():
    while True:
        print("\n=== Product Management System ===")
        print("1. Add Product")
        print("2. List Products")
        print("3. Delete Product")
        print("4. Update Product Price")
        print("5. Apply Discount to All Products")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            id = int(input("Enter product id: "))
            name = input("Enter product name: ")

            try:
                price = float(input("Enter product price: "))
                add_product(id, name, price)
            except ValueError:
                print("Invalid price entered. Please enter a number.")
        elif choice == '2':
            list_products()
        elif choice == '3':
            try:
                id = int(input("Enter product id: "))
                delete_product(id)
            except ValueError:
                print("Invalid price id. Please enter a number.")
        elif choice == '4':
            product_id = int(input("Enter product ID: "))
            new_price = float(input("Enter new price: "))
            update_product_price(product_id, new_price)
        elif choice == '5':
            discount = float(input("Enter discount percentage: "))
            apply_discount(discount)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
