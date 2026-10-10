# Library Management System using Python and MySQL

This project is a console-based Library Management System developed using Python, Object-Oriented Programming (OOP), and MySQL.

I built this project to manage books, library members, book locations, and borrowing transactions. It supports CRUD operations and stores all the information in a MySQL database.

## Features

- **Book Management:** Add, view, search, update, and delete books.
- **User Management:** Manage library member details.
- **Location Management:** Organize books using Row, Rack, and Shelf locations.
- **Transaction Management:** Handle book borrowing and returns.
- **Book Availability:** Track available book quantities.
- **Database Setup:** Automatically create the database and required tables.
- **Error Handling:** Handle invalid inputs and database errors.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- MySQL
- MySQL Connector
- Python-dotenv

## Project Structure

```text
Library-Management-System/
│
├── config/
│   ├── db.py
│   ├── schema.py
│   └── confiq.py
│
├── models/
│   ├── book.py
│   ├── user.py
│   ├── master.py
│   ├── row.py
│   ├── rack.py
│   ├── shelf.py
│   └── transaction.py
│
├── services/
│   └── library.py
│
├── main.py
├── .env.example
└── README.md
```

## How It Works

1. Library members and books are added to the system.
2. Books are assigned to specific rows, racks, and shelves.
3. When a book is borrowed, its available quantity is reduced.
4. When a book is returned, its available quantity is increased.
5. All records and transactions are maintained in MySQL.

## How to Run

**1. Clone the repository**

```bash
git clone https://github.com/SachinDevarajan/Library-Management-System.git
cd Library-Management-System
```

**2. Install the required libraries**

```bash
pip install mysql-connector-python python-dotenv
```

**3. Configure the database**

Create a `.env` file using `.env.example` and add your MySQL credentials.

```env
LIBRARY_DB_HOST=localhost
LIBRARY_DB_USER=root
LIBRARY_DB_PASSWORD=your_password
LIBRARY_DB_NAME=your_database
```

The application automatically creates the database and required tables.

**4. Run the application**

```bash
python main.py
```

## What I Learned

Through this project, I gained practical experience in:

- Python OOP concepts
- MySQL database connectivity
- CRUD operations
- Database relationships
- Exception handling
- Organizing Python code into modules
- Managing data using SQL queries

## Author

**Sachin Devarajan**

GitHub: [SachinDevarajan](https://github.com/SachinDevarajan)

LinkedIn: [Sachin Devarajan](https://linkedin.com/in/sachindevarajan)
