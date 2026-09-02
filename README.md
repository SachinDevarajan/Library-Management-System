# 📚 Library Management System

A console-based **Library Management System** built with **Python**, **Object-Oriented Programming**, and **MySQL** — designed to manage books, users, physical storage locations, and borrowing transactions through a clean, modular CLI.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![OOP](https://img.shields.io/badge/OOP-Object--Oriented-7B2CBF?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Automatic Schema Creation](#automatic-schema-creation)
- [Error Handling](#error-handling)
- [Core Workflows](#core-workflows)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Environment Configuration](#environment-configuration)
- [Sample Data](#sample-data)
- [What I Learned](#what-i-learned)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Author](#author)

---

## Overview

This project simulates the core operations of a real-world library: managing a book catalog, tracking user records, organizing physical shelf locations, and recording the full lifecycle of borrowing and returning books. It's built to demonstrate how Python's OOP principles translate into a working, database-backed CRUD application — with a clear separation between data models, business logic, database setup, and the connection layer.

**Goals:**
- Efficiently manage and search a book catalog
- Maintain accurate user records
- Track real-time book availability and shelf capacity
- Model physical library locations (Row → Rack → Shelf)
- Record and audit borrow/return transactions
- Persist all data reliably in MySQL
- Set up its own database schema automatically — no manual SQL required

---

## Features

### 📚 Book Management
Add, view, search, update, and remove books. Each record tracks title, author, publisher, category, total quantity, available quantity, and its physical shelf location. Adding a book validates the shelf's remaining capacity and automatically reduces it as the shelf fills up.

### 👤 User Management
Add, view, search, update, and remove library members.

### 🗄️ Location Management
Books are mapped to a physical hierarchy:

```
Master
 └── Row
      └── Rack
           └── Shelf
```

Each level is modeled as its own class, so any book can be traced to its exact physical spot on a shelf. Shelf capacity is tracked and decremented as it's filled, preventing overfilled shelves.

### 🔄 Transaction Management
Borrow and return books with automatic availability tracking, plus search and full transaction history.

### 🛠️ Self-Setting-Up Database
On first run, the app creates its own MySQL database and every required table automatically — nothing needs to be created manually beforehand.

### 🛡️ Defensive Error Handling
Every user input and database operation across the entire service layer is wrapped in try/except, with automatic rollback on failure, so invalid input or database errors never crash the app.

---

## Architecture

```
                    ┌─────────────────────┐
                    │      main.py        │
                    │   CLI Application   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  services/library    │
                    │   Business Logic     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
        ┌──────────┐     ┌──────────┐     ┌──────────┐
        │  Models  │     │ Database │     │  CRUD    │
        │          │     │  (MySQL) │     │Operations│
        └──────────┘     └────┬─────┘     └──────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ config/schema │
                        │ Table setup   │
                        └──────────────┘
```

The CLI layer never talks to the database directly — every request flows through the `Library` service, which coordinates the data models and the MySQL connection. Database connection setup and schema (table) creation are kept in separate config modules, keeping the code testable and easy to extend.

---

## Project Structure

```
Library-Management-System/
│
├── config/
│   ├── db.py            # MySQL connection + database creation
│   ├── schema.py         # All CREATE TABLE definitions
│   └── confiq.py         # App configuration (env vars)
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
│   └── library.py        # Core business logic (with full error handling)
│
├── .env.example
├── .gitignore
├── main.py                # CLI entry point
└── README.md
```

---

## Database Design

Connectivity is handled through `mysql.connector`.

```
Python Application
       │
       ▼
mysql.connector
       │
       ▼
      MySQL
```

Every book is linked to a `master_id`, which resolves to a specific **Row → Rack → Shelf** combination — giving each catalog entry a precise physical address inside the library.

---

## Automatic Schema Creation

`config/db.py` and `config/schema.py` together mean you never need to run SQL by hand:

1. **`config/db.py`** connects to the MySQL server (no database selected) and runs `CREATE DATABASE IF NOT EXISTS`.
2. It then reconnects with that database selected, producing the shared `connection` and `cursor` used everywhere.
3. **`config/schema.py`** defines `create_tables(connection, cursor)`, which runs `CREATE TABLE IF NOT EXISTS` for every table in the correct dependency order:

   ```
   row_table → rack → shelf → master → books
                                users → transactions
   ```

4. `db.py` calls `create_tables()` automatically the moment it's imported.

So the first time you run `main.py` against a fresh MySQL server, the database and every table are created for you. On every later run, the same calls simply verify the tables already exist and the app continues straight to the menu — nothing is dropped or duplicated.

---

## Error Handling

Every method in `services/library.py` follows the same defensive pattern:

- **User input** (`int(input(...))`, etc.) is wrapped in `try/except ValueError`, so non-numeric input prints a clear message instead of crashing.
- **Database operations** are wrapped in `try/except Exception` with `connection.rollback()` on failure, so a failed query never leaves partially-committed data.
- **Shelf capacity** is validated before inserting a book (quantity must be positive and within the shelf's remaining capacity) and is automatically decremented after a successful insert.

---

## Core Workflows

### Adding a Book

```
Select Shelf → Check Remaining Capacity
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       Exceeds Capacity      Fits on Shelf
                                   │
                                   ▼
                          Insert Book Record
                                   │
                                   ▼
                    Reduce Shelf's Remaining Capacity
```

### Borrowing a Book

```
Select Book → Check Availability
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Not Available        Available
                             │
                             ▼
                    Create Transaction
                             │
                             ▼
                Reduce Available Quantity
```

### Returning a Book

```
Return Request → Find Transaction → Update Transaction
                                            │
                                            ▼
                                Increase Available Quantity
                                            │
                                            ▼
                                  Book Available Again
```

---

## Tech Stack

| Category      | Tools                          |
|---------------|---------------------------------|
| Language       | Python                         |
| Database       | MySQL                          |
| Architecture   | Object-Oriented Programming     |
| Version Control| Git, GitHub                    |
| Editor         | VS Code                        |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SachinDevarajan/Library-Management-System.git
cd Library-Management-System
```

### 2. Verify Python is installed

```bash
python --version
```

### 3. Install dependencies

```bash
pip install mysql-connector-python python-dotenv
```

### 4. Configure your database credentials

Copy `.env.example` to `.env` and fill in your MySQL credentials — see [Environment Configuration](#environment-configuration).

> ⚠️ **Never commit real database credentials to GitHub.**

You do **not** need to manually create the database or tables — the app creates them automatically on first run (see [Automatic Schema Creation](#automatic-schema-creation)).

### 5. Run the application

```bash
python main.py
```

---

## Environment Configuration

Copy `.env.example` to `.env` and fill in your own values:

```env
LIBRARY_DB_HOST=localhost
LIBRARY_DB_USER=your_username
LIBRARY_DB_PASSWORD=your_password
LIBRARY_DB_NAME=your_database
```

---

## Sample Data

```
Book ID    : 101
Title      : Python Basics
Author     : Mark Lutz
Publisher  : Example Publisher
Category   : Programming
Quantity   : 10
Available  : 10

Location
  Master ID : 111
  Row ID    : 1
  Rack ID   : 1
  Shelf ID  : 1
```

---

## What I Learned

- Structuring a multi-module Python application around OOP principles
- Integrating Python with MySQL for persistent, relational data storage
- Designing and implementing CRUD workflows end-to-end
- Modeling real-world hierarchies (Row → Rack → Shelf) in code
- Separating business logic, models, schema definition, and database access cleanly
- Automating database/table setup so the app is runnable with zero manual SQL
- Writing defensive, production-style error handling around user input and database calls
- Managing configuration securely with environment variables

---

## Roadmap

- [ ] Web-based interface
- [ ] User authentication and role-based access
- [ ] Analytics dashboard for library usage
- [ ] Due-date reminders and fine calculation
- [ ] Email notifications
- [ ] Advanced multi-field search
- [ ] Automated unit tests
- [ ] Docker support
- [ ] REST API
- [ ] Cloud database deployment

---

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## Author

**Sachin Devarajan**
Data Analyst · Data Engineer · Machine Learning Enthusiast

Python · SQL · Power BI · Machine Learning · PySpark

[GitHub](https://github.com/SachinDevarajan) · [LinkedIn](https://linkedin.com/in/sachindevarajan)

---

⭐ If you found this project useful, consider giving it a star!
