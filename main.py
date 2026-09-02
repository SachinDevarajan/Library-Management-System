from services.library import Library

library = Library()

def row_menu(library):
    while True:
        print("\n===== Row Management=====")
        print()
        print("1. Add Row")
        print("2. View Rows")
        print("3. Search Row")
        print("4. Update Row")
        print("5. Delete Row")
        print("6. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.add_row()
            case 2:
                library.view_rows()
            case 3:
                library.search_row()
            case 4:
                library.update_row()
            case 5:
                library.delete_row()
            case 6:
                return
            case _:
                print("Invalid Choice")

def rack_menu(library):
    while True:
        print("\n===== Rack Management=====")
        print()
        print("1. Add Rack")
        print("2. View Racks")
        print("3. Search Rack")
        print("4. Update Rack")
        print("5. Delete Rack")
        print("6. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.add_rack()
            case 2:
                library.view_racks()
            case 3:
                library.search_rack()
            case 4:
                library.update_rack()
            case 5:
                library.delete_rack()
            case 6:
                return
            case _:
                print("Invalid Choice")

def shelf_menu(library):
    while True:
        print("\n===== Shelf Management=====")
        print()
        print("1. Add Shelf")
        print("2. View Shelfs")
        print("3. Search Shelf")
        print("4. Update Shelf")
        print("5. Delete Shelf")
        print("6. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.add_shelf()
            case 2:
                library.view_shelfs()
            case 3:
                library.search_shelf()
            case 4:
                library.update_shelf()
            case 5:
                library.delete_shelf()
            case 6:
                return
            case _:
                print("Invalid Choice")

def book_menu(library):
    while True:
        print("\n===== Book Management=====")
        print()
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Remove Book")
        print("6. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.add_book()
            case 2:
                library.view_books()
            case 3:
                library.search_book()
            case 4:
                library.update_book()
            case 5:
                library.remove_book()
            case 6:
                return
            case _:
                print("Invalid Choice")

def user_menu(library):
    while True:
        print("\n===== User Management=====")
        print()
        print("1. Add User")
        print("2. View Users")
        print("3. Search User")
        print("4. Update User")
        print("5. Remove User")
        print("6. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.add_user()
            case 2:
                library.view_users()
            case 3:
                library.search_user()
            case 4:
                library.update_user()
            case 5:
                library.remove_user()
            case 6:
                return
            case _:
                print("Invalid Choice")

def transaction_menu(library):
    while True:
        print("\n===== Transaction Management=====")
        print()
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. View Transactions")
        print("4. Search Transaction")
        print("5. Back")

        choice = int(input("Enter Choice : "))
        match choice :
            case 1:
                library.borrow_book()
            case 2:
                library.return_book()
            case 3:
                library.view_transactions()
            case 4:
                library.search_transaction()
            case 5:
                return
            case _:
                print("Invalid Choice")

while True:
    print("\n===== Library Management System =====")
    print()
    print("1. Row Management")
    print("2. Rack Management")
    print("3. Shelf Management")
    print("4. Book Management")
    print("5. User Management")
    print("6. Transaction Management")
    print("7. Exit")
    print()

    choice = int(input("Enter Choice : "))
    match choice :
        case 1:
            row_menu(library)
        case 2:
            rack_menu(library)
        case 3:
            shelf_menu(library)
        case 4:
            book_menu(library)
        case 5:
            user_menu(library)
        case 6:
            transaction_menu(library)
        case 7:
            break
        case _:
            print("Invalid Selection")