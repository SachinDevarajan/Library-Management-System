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

This project simulates the core operations of a real-world library: managing a book catalog, tracking user records, organizing physical shelf locations, and recording the full lifecycle of borrowing and returning books. It's built to demonstrate how Python's OOP principles translate into a working, database-backed CRUD application — with a clear separation between data models, business logic, and the database layer.

**Goals:**
- Efficiently manage and search a book catalog
- Maintain accurate user records
- Track real-time book availability
- Model physical library locations (Row → Rack → Shelf)
- Record and audit borrow/return transactions
- Persist all data reliably in MySQL

---

## Features

### 📚 Book Management
Add, view, search, update, and remove books. Each record tracks title, author, publisher, category, total quantity, available quantity, and its physical shelf location.

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

Each level is modeled as its own class, so any book can be traced to its exact physical spot on a shelf.

### 🔄 Transaction Management
Borrow and return books with automatic availability tracking, plus search and full transaction history.

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
        └──────────┘     └──────────┘     └──────────┘
```

The CLI layer never talks to the database directly — every request flows through the `Library` service, which coordinates the data models and the MySQL connection. This keeps the code testable and easy to extend.

---

## Project Structure

```
Library-Management-System/
│
├── config/
│   ├── db.py           # MySQL connection setup
│   └── confiq.py        # App configuration
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
│   └── library.py       # Core business logic
│
├── .env.example
├── .gitignore
├── main.py               # CLI entry point
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

## Core Workflows

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
pip install mysql-connector-python
```

### 4. Set up the database

Create a MySQL database and configure your connection using the `.env.example` file as a reference.

> ⚠️ **Never commit real database credentials to GitHub.**

### 5. Run the application

```bash
python main.py
```

---

## Environment Configuration

Copy `.env.example` to `.env` and fill in your own values:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
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
- Separating business logic, models, and database access cleanly
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
