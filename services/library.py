from models.book import Book
from models.user import User
from models.transaction import Transaction
from models.row import Row
from models.rack import Rack
from models.shelf import Shelf
from config.db import connection, cursor

from datetime import date,timedelta

class Library:
    """
    Book Section
    """
    def add_book(self):
        self.view_shelfs()
        try:
            title = input("Enter Book Title : ")
            author = input("Enter Author Name : ")
            publisher = input("Enter Publisher Name : ")
            category = input("Enter Category : ")
            quantity = int(input("Enter Quantity : "))
            shelf_id = int(input("Enter Shelf ID : "))
        except Exception as e:
            print("Error : ",e)
        
        query = '''select s.shelf_id, r.rack_id, rt.row_id, s.capacity
                    from shelf s join rack r on s.rack_id = r.rack_id 
                    join row_table rt on r.row_id = rt.row_id
                    where s.shelf_id = %s'''
        cursor.execute(query,(shelf_id,))
        location = cursor.fetchone()
        if not location:
            print("Invalid Shelf ID")
            return
        shelf_id = location[0]
        rack_id = location[1]
        row_id = location[2]
        capacity = location[3]

        if quantity > capacity:
            print("Quantity exceeds shelf capacity")
            print(f"Shelf Capacity : {capacity}")
            return

        master_id = int(f'{row_id}{rack_id}{shelf_id}')
        cursor.execute('select master_id from master where master_id = %s',(master_id,))
        master = cursor.fetchone()
        if master is None:
            query = '''insert into master (master_id,row_id,rack_id,shelf_id) values(%s,%s,%s,%s)'''
            cursor.execute(query,(master_id,row_id,rack_id,shelf_id))
            
            query = """
                INSERT INTO books
                (title, author,publisher,category, quantity, available,master_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            values = (title, author, publisher, category, quantity, quantity, master_id)
            try:
                cursor.execute(query, values)
                connection.commit()
                print("Book Added Successfully")
            except Exception as e:
                print("Error:", e)
                

    def view_books(self):
        query = '''
            select b.book_id, b.title, b.author, b.publisher, b.category, b.quantity, b.available, m.shelf_id, m.rack_id, m.row_id , m.master_id
            from books b join master m on b.master_id = m.master_id
            order by b.book_id
            '''
        cursor.execute(query)
        books = cursor.fetchall()

        if not books:
            print("No Books Available")
            return

        for book in books:
            print(f"Book ID         : {book[0]}")
            print(f"Title           : {book[1]}")
            print(f"Author Name     : {book[2]}")
            print(f"Publisher Name  : {book[3]}")
            print(f"Category        : {book[4]}")
            print(f"Quantity        : {book[5]}")
            print(f"Available       : {book[6]}")
            print("---Location---")
            print(f"Master ID       : {book[10]}")
            print(f"Row ID          : {book[9]}")
            print(f"Rack ID         : {book[8]}")
            print(f"Shelf ID        : {book[7]}")
            print("---------------------------------")            


    def search_book(self):
        book_id = int(input("Enter a Book ID : "))
        query = '''SELECT * from books where book_id=%s'''
        cursor.execute(query,(book_id,))
        row = cursor.fetchone()
        if row is None:
            print("Book Not Found")
            return
        print()
        print(f"Book ID     : {row[0]}")
        print(f"Title       : {row[1]}")
        print(f"Author      : {row[2]}")
        print(f"Publisher   : {row[3]}")
        print(f"Category    : {row[4]}")
        print(f"Quantity    : {row[5]}")
        print(f"Available   : {row[6]}")
        print(f"Master ID   : {row[7]}")
        print("---------------------")

    def update_book(self):
        book_id = int(input("Enter Book ID : "))
        query = "SELECT * FROM books WHERE book_id = %s"
        cursor.execute(query, (book_id,))
        row = cursor.fetchone()

        if row is None:
            print("Book Not Found")
            return

        while True:
            print("\n1. Update Title")
            print("2. Update Author")
            print("3. Update Category")
            print("4. Update Quantity")
            print("5. Update Publisher")
            print("6. Update Location")
            print("7. Exit")

            choice = int(input("Enter your choice : "))
            match choice:
                case 1:
                    title = input("Enter New Title : ")
                    cursor.execute("UPDATE books SET title = %s WHERE book_id = %s",(title, book_id))
                    connection.commit()
                    print("Title Updated Successfully")

                case 2:
                    author = input("Enter New Author : ")
                    cursor.execute("UPDATE books SET author = %s WHERE book_id = %s",(author, book_id))
                    connection.commit()
                    print("Author Updated Successfully")

                case 3:
                    category = input("Enter New Category : ")
                    cursor.execute("UPDATE books SET category = %s WHERE book_id = %s", (category, book_id))
                    connection.commit()
                    print("Category Updated Successfully")

                case 4:
                    query = """SELECT quantity, available FROM books WHERE book_id = %s """
                    cursor.execute(query, (book_id,))
                    book_data = cursor.fetchone()
                    old_quantity = book_data[0]
                    old_available = book_data[1]
                    borrowed = old_quantity - old_available
                    new_quantity = int(input("Enter New Quantity : ") )

                    if new_quantity < borrowed:
                        print(f"Cannot reduce quantity below {borrowed}.")
                        continue
                    new_available = new_quantity - borrowed
                    query = """UPDATE books SET quantity = %s, available = %s WHERE book_id = %s """
                    cursor.execute(query,(new_quantity, new_available, book_id))
                    connection.commit()
                    print("Quantity Updated Successfully")

                case 5:
                    publisher = input( "Enter New Publisher : " )
                    cursor.execute("""UPDATE books SET publisher = %s WHERE book_id = %s """, (publisher, book_id))
                    connection.commit()
                    print("Publisher Updated Successfully")

                case 6:
                    self.view_shelfs()
                    shelf_id = int(input("Enter New Shelf ID : "))
                    query = """ 
                            SELECT s.shelf_id, r.rack_id, r.row_id
                            FROM shelf s JOIN rack r ON s.rack_id = r.rack_id
                            WHERE s.shelf_id = %s
                        """
                    cursor.execute(query, (shelf_id,))
                    location = cursor.fetchone()
                    if location is None:
                        print("Invalid Shelf ID")
                        continue

                    shelf_id = location[0]
                    rack_id = location[1]
                    row_id = location[2]
                    master_id = int(f"{row_id}{rack_id}{shelf_id}")

                    query = """ SELECT master_id FROM master WHERE master_id = %s """
                    cursor.execute( query, (master_id,))
                    master = cursor.fetchone()
                    if master is None:
                        query = """ INSERT INTO master (master_id, row_id, rack_id, shelf_id) VALUES (%s, %s, %s, %s)"""
                        cursor.execute( query, (master_id, row_id, rack_id, shelf_id ))

                    query = """UPDATE books SET master_id = %s WHERE book_id = %s """
                    cursor.execute( query, (master_id, book_id))
                    connection.commit()
                    print("Book Location Updated Successfully")
                    print(f"Row ID    : {row_id}")
                    print(f"Rack ID   : {rack_id}")
                    print(f"Shelf ID  : {shelf_id}")
                    print(f"Master ID : {master_id}")

                case 7:
                    return

                case _:
                    print("Invalid Choice")

    def remove_book(self):
        book_id = int(input("Enter Book ID : "))
        cursor.execute('select * from books where book_id = %s',(book_id,))
        data = cursor.fetchone()
        if not data:
            print("Book Not found")
            return
        user = Book(*data)
        print("Book Found")
        user.display()
        confirm  = input("Are you sure Delete this Book ?(y/n) : ")
        if confirm.lower() != 'y':
            print("Book Removing Cancelled")
            return
        
        query = "DELETE from books where book_id = %s"
        cursor.execute(query,(book_id,))
        connection.commit()
        print("Book Successfully removed")


    """
    user Section
    """

    def add_user(self):
        name = input("Enter User Name : ")
        phone = input("Enter Phone Number : ")
        email = input("Enter Email : ")
        role = input("User Role : ")
        doj = date.today()
        query = '''insert into users (name, phone, email, role, doj) values(%s,%s,%s,%s,%s)'''
        cursor.execute(query,(name,phone,email,role,doj))
        connection.commit()
        print("USer Added Successfuly...")

    def view_users(self):
        cursor.execute('select * from users')
        users = cursor.fetchall()
        if not users:
            print("No Users Available")
            return
        for data in users:
            user = User(*data)
            user.display()
            print('-------------------------')
    
    def search_user(self):
        user_id = int(input('Enter User ID : '))
        query = '''select * from users where user_id = %s'''
        cursor.execute(query,(user_id,))
        data = cursor.fetchone()
        if not data:
            print("User Not Found")
            return
        user = User(*data)
        user.display()

    def update_user(self):
        user_id = int(input("Enter User ID : "))
        cursor.execute('select * from users where user_id = %s',(user_id,))
        data = cursor.fetchone()
        if not data:
            print("User Not Found")
            return
        while True:
            print("1. Update Name ")
            print("2. Update Phone ")
            print("3. Update Email ")
            print("4. Update Role ")
            print("5. Exit ")
            choice = int(input('Enter Choice : '))
            match choice:
                case 1:
                    name = input("Enter New Name : ")
                    cursor.execute('update users set name = %s where user_id = %s',(name,user_id))
                    connection.commit()
                    print("User name updated successfully")
                case 2:
                    phone = input("Enter Phone Number : ")
                    cursor.execute('update users set phone = %s where user_id = %s',(phone,user_id))
                    connection.commit()
                    print("User Phone Number updated successfully")
                case 3:
                    email = input("Enter Email : ")
                    cursor.execute('update users set email = %s where user_id = %s',(email,user_id))
                    connection.commit()
                    print("User Email updated successfully")
                case 4:
                    role = input("Enter Role : ")
                    cursor.execute('update users set role = %s where user_id = %s',(role,user_id))
                    connection.commit()
                    print("User Role updated successfully")  
                case 5:
                    return
                case _:
                    print("Invalid Selection")


    def remove_user(self):
            user_id = int(input("Enter User ID : "))
            cursor.execute('select * from users where user_id = %s',(user_id,))
            data = cursor.fetchone()
            if not data:
                print("User Not found")
                return
            user = User(*data)
            print("User Found")
            user.display()
            confirm  = input("Are you sure Delete this User ?(y/n) : ")
            if confirm.lower() != 'y':
                print("User Removing Cancelled")
                return
            
            query = "DELETE from users where user_id = %s"
            cursor.execute(query,(user_id,))
            connection.commit()
            print("User Successfully removed")

    """
    Borrow & Return Transaction
    """
    def borrow_book(self):
        user_id = int(input("Enter User ID : "))
        book_id = int(input("Enter Book ID : "))
        cursor.execute('select user_id from users where user_id = %s',(user_id,))
        user = cursor.fetchone()
        if not user:
            print("User Not Found")
            return
        cursor.execute('select book_id,available from books where book_id = %s',(book_id,))
        book = cursor.fetchone()
        if not book:
            print("Book Not Found")
            return

        if book[1] <= 0 :
            print("Book Not Available")
            return
        query = '''select transaction_id from transactions where user_id = %s and book_id =%s and status = "Issued"'''
        cursor.execute(query,(user_id,book_id))
        existing = cursor.fetchone()
        if existing:
            print("Member Already Borrowed this Book")
            return
        
        issue_date = date.today()
        due_date = issue_date + timedelta(days=10)
        query = '''update books set available = available-1 where book_id = %s'''
        cursor.execute(query,(book_id,))

        query = '''insert into transactions (user_id, book_id, issue_date, due_date) values (%s,%s,%s,%s)'''
        cursor.execute(query,(user_id,book_id,issue_date,due_date))
        connection.commit()
                
        print("Book borrowed Successfully...")
        print("Issue Date : ",issue_date)
        print("Due Date : ",due_date)


    def return_book(self):
        transaction_id = int(input('Enter Transaction ID : '))
        query = '''
                select transaction_id, user_id, book_id, due_date 
                from transactions
                where transaction_id = %s and status='Issued'
                '''
        cursor.execute(query,(transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            print("Transaction Not Found")
            return
        book_id = transaction[2]
        return_date = date.today()
        query = '''update transactions set return_date = %s, status = 'Returned' 
                    where transaction_id = %s'''
        cursor.execute(query,(return_date,transaction_id))

        query = '''update books set available= available+1 where book_id = %s'''
        cursor.execute(query,(book_id,))
        connection.commit()
        print('Book Returned Successfully')
        

    def view_transactions(self):
        query = '''
                select t.transaction_id, u.name, b.title, t.issue_date, t.due_date, t.return_date, t.status
                from transactions t join users u on t.user_id = u.user_id
                join books b on t.book_id = b.book_id 
                order by t.transaction_id
                '''
        cursor.execute(query)
        transactions = cursor.fetchall()
        if not transactions:
            print("No Transactions Available")
            return
        for transaction in transactions:
            print(f'Transaction ID  : {transaction[0]}')
            print(f'User Name       : {transaction[1]}')
            print(f'Book Title      : {transaction[2]}')
            print(f'Issue Date      : {transaction[3]}')
            print(f'Due Date        : {transaction[4]}')
            print(f'Return Date     : {transaction[5]}')
            print(f'Status          : {transaction[6]}')
            print("-------------------------------------")


    def search_transaction(self):
        transaction_id = int(input("Enter Transaction ID : "))
        query = '''select * from transactions 
                    where transaction_id = %s
                '''
        cursor.execute(query,(transaction_id,))
        transactions = cursor.fetchone()
        if not transactions:
            print("No Transaction Available")
            return
        transaction = Transaction(*transactions)
        transaction.display()
                

    """
    Rows
    """

    def add_row(self):
        row_name = input("Enter the Row Name : ")
        query = """insert into row_table (row_name) values(%s)"""
        cursor.execute(query,(row_name,))
        connection.commit()
        print("Row added Successfully")

    def view_rows(self):
        quary = '''select * from row_table order by row_id'''
        cursor.execute(quary)
        rows = cursor.fetchall()
        if not rows:
            print("No rows Available")
            return
        for row in rows:
            detail = Row(*row)
            detail.display()
            print('-------------------------------')

    def search_row(self):
        row_id = int(input('Enter Row ID : '))
        query = """select * from row_table where row_id=%s"""
        cursor.execute(query,(row_id,))
        row = cursor.fetchone()
        if row:
            details = Row(*row)
            details.display()
        else:
            print("Row not Found")


    def update_row(self):
        row_id = int(input('Enter Row ID : '))
        query = """select * from row_table where row_id=%s"""
        cursor.execute(query,(row_id,))
        row = cursor.fetchone()
        if row is None:
            print("Row not Found")
            return
        
        row_name = input('Enter New Row Name : ')
        query = '''update row_table set row_name = %s where row_id = %s'''
        cursor.execute(query,(row_name,row_id))
        connection.commit()
        print("Row updated Successfully")


    def delete_row(self):
        row_id = int(input('Enter Row ID : '))
        query = '''select * from rack where rack_id = %s'''
        cursor.execute(query,(row_id,))
        racks = cursor.fetchall()
        if racks:
            print("Cannot Delete this Row")
            print("Racks are assigned to this Row")
            return

        query = """select * from row_table where row_id = %s"""
        cursor.execute(query,(row_id,))
        row = cursor.fetchone()

        if row is None:
            print("Row not Found")
            return
        query = '''delete from row_table where row_id = %s'''
        cursor.execute(query,(row_id,))
        connection.commit()
        print("Row deleted Successfully")


    """
    Rack Table
    """
    def add_rack(self):
        self.view_rows()
        row_id = int(input("Enter Row ID : "))
        rack_name = input('Enter Rack Name : ')
        query = '''select * from row_table where row_id = %s'''
        cursor.execute(query,(row_id,))
        row = cursor.fetchone()

        if row is None:
            print("Invalid Row ID")
            return
        query = '''insert into rack(row_id,rack_name) values(%s,%s)'''
        cursor.execute(query,(row_id,rack_name))
        connection.commit()
        print("Rack Added Successfully")

    def view_racks(self):
        query = '''
                select r.rack_id, r.rack_name, r.row_id from rack r join row_table rt
                on r.row_id = rt.row_id             
                '''
        cursor.execute(query)
        racks = cursor.fetchall()
        if not racks:
            print("No Racks Available")
            return
        for rack in racks:
            details = Rack(*rack)
            details.display()
            print("---------------------")

    def search_rack(self):
        rack_id = int(input("Enter Rack ID : "))
        query = '''
                select r.rack_id,r.rack_name,row_id from rack r join row_table rt
                on r.row_id = rt.row_id 
                where rack_id = %s           
                '''
        cursor.execute(query,(rack_id,))
        rack = cursor.fetchone()
        if rack:
            details = Rack(*rack)
            details.display()
            print("---------------------")
        else:
            print("Book Not Found")

    def update_rack(self):
        rack_id = int(input("Enter Rack ID : "))
        query = '''
                select * from rack where rack_id = %s
                '''
        cursor.execute(query,(rack_id,))
        rack = cursor.fetchone()

        if rack is None:
            print('Rack Not Found')
            return
        while True:
            print('1. Update Rack Name\n2. Change Row\n3. Exit')
            choice = int(input('Enter Choice : '))
            match choice:
                case 1:
                    rack_name = input("Enter New Rack Name : ")
                    query = '''update rack set rack_name = %s
                            where rack_id = %s
                            '''
                    cursor.execute(query,(rack_name,rack_id))
                    connection.commit()
                    print("Rack Name Updated successfully")
                case 2:
                    self.view_rows()
                    row_id = int(input('Enter New Row ID : '))
                    query = '''select * from row_table where row_id = %s'''
                    cursor.execute(query,(row_id,))
                    row = cursor.fetchone()
                    if row is None:
                        print("Invalid Row ID")
                        continue
                    query = '''update rack set row_id = %s where rack_id = %s'''
                    cursor.execute(query,(row_id,rack_id))
                    connection.commit()
                    print("Row Changed Successfully")
                case 3:
                    return
                case _:
                    print("Invalid Chice")


    def delete_rack(self):
        rack_id = int(input('Enter Rack ID : '))
        query = '''select * from shelf where rack_id= %s'''
        cursor.execute(query,(rack_id,))
        shelfs = cursor.fetchall()
        if shelfs:
            print("Cannot Delete this Rack")
            print("Shelfs are assigned to this Rack")
            return

        query = '''select * from rack where rack_id = %s'''
        cursor.execute(query,(rack_id,))
        rack = cursor.fetchone()
        if rack is None:
            print("Rack Not Found")
            return
        
        query = 'delete from rack where rack_id = %s'
        cursor.execute(query,(rack_id,))
        connection.commit()
        print("Rack Deleted Successfully")

    '''
    Shelf
    '''
    def add_shelf(self):
        self.view_racks()
        rack_id = int(input('Enter Rack ID : '))
        capacity = int(input('Enter Shelf Capacity : '))
        query = '''select * from rack where rack_id = %s'''
        cursor.execute(query,(rack_id,))
        rack = cursor.fetchone()
        if rack is None:
            print("Invalid Rack ID")
            return
        query =  '''insert into shelf(rack_id,capacity) values (%s,%s)'''
        cursor.execute(query,(rack_id,capacity))
        connection.commit()
        print("Shelf Added Successfully")

    def view_shelfs(self):
        query = '''
                select s.shelf_id, r.rack_name, rt.row_name, s.capacity
                from shelf s join rack r on s.rack_id = r.rack_id
                join row_table rt on r.row_id = rt.row_id
                '''
        cursor.execute(query)
        shelfs = cursor.fetchall()
        if not shelfs:
            print("No shelfs Available")
            return 
        for shelf in shelfs:
            print(f"Shelf ID    : {shelf[0]}")
            print(f"Rack Name   : {shelf[1]}")
            print(f"Row Name    : {shelf[2]}")
            print(f"Capacity    : {shelf[3]}")
            print("----------------------------")

    def search_shelf(self):
        shelf_id = int(input("Enter Shelf ID : "))
        query = '''
                select s.shelf_id, s.shelf_name, r.rack_name, rt.row_name, s.capacity
                from shelf s join rack r on s.rack_id = r.rack_id
                join row_table rt on r.row_id = rt.row_id 
                where s.shelf_id = %s
                '''
        cursor.execute(query,(shelf_id,))
        shelf = cursor.fetchone()
        if shelf:
            print(f"Shelf ID    : {shelf[0]}")
            print(f"Shelf Name  : {shelf[1]}")
            print(f"Rack Name   : {shelf[2]}")
            print(f"Row Name    : {shelf[3]}")
            print(f"Capacity    : {shelf[4]}")
            print("----------------------------")
        else:
            print("Shelf Not found")

    def update_shelf(self):
        shelf_id = int(input("Enter Shelf ID : "))
        query = '''select * from shelf where shelf_id = %s'''
        cursor.execute(query,(shelf_id,))
        shelf = cursor.fetchone()
        if shelf is None:
            print("Shelf Not Found")
            return
        while True:
            print("1. Update Shelf Name ")
            print("2. Update Capacity")
            print("3. Change Rack ")
            print("4. Exit ")
            choice = int(input("Enter Choice : "))
            match choice:
                case 1:
                    shelf_name = input("Enter New Shelf Name : ")
                    query = '''update shelf set shelf_name %s where shelf_id = %s'''
                    cursor.execute(query,(shelf_name,shelf_id))
                    connection.commit()
                    print("Shelf Name Changed Successfully")
                case 2:
                    capacity = input("Enter New Capacity : ")
                    query = '''update shelf set capacity = %s where shelf_id = %s'''
                    cursor.execute(query,(capacity,shelf_id))
                    connection.commit()
                    print("Capacity Changed Successfully")
                case 3:
                    self.view_racks()
                    rack_id = int(input("Enter New Rack ID : "))
                    query = '''select * from rack where rack_id = %s'''
                    cursor.execute(query,(rack_id,))
                    rack = cursor.fetchone()
                    if rack is None:
                        print("Invalid Rack ID")
                        continue
                    query = '''update shelf set rack_id = %s where shelf_id = %s'''
                    cursor.execute(query,(rack_id,shelf_id))
                    connection.commit()
                    print("Shelf Name Changed Successfully")
                case 4:
                    return 
                case _:
                    print("Invalid Choice")

    def delete_shelf(self):
        shelf_id = int(input("Enter Shelf ID : "))
        query = '''select * from books where shelf_id= %s'''
        cursor.execute(query,(shelf_id,))
        books = cursor.fetchall()
        if books:
            print("Cannot Delete this Shelf")
            print("Books are assigned to this Shelf")
            return

        query = '''select * from shelf where shelf_id = %s'''
        cursor.execute(query,(shelf_id,))
        shelf = cursor.fetchone()
        if shelf is None:
            print("Shelf not Found")
            return
        details = Shelf(*shelf)
        details.display()
        print("---------------------")

        query = '''delete from shelf where shelf_id = %s'''
        cursor.execute(query,(shelf_id,))
        connection.commit()
        print("Shelf Deleted Successfully")

    