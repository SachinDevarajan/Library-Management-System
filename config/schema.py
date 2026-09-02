def create_tables(connection, cursor):
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS row_table (
            row_id INT AUTO_INCREMENT PRIMARY KEY,
            row_name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rack (
            rack_id INT AUTO_INCREMENT PRIMARY KEY,
            row_id INT NOT NULL,
            rack_name VARCHAR(100) NOT NULL,
            FOREIGN KEY (row_id) REFERENCES row_table(row_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS shelf (
            shelf_id INT AUTO_INCREMENT PRIMARY KEY,
            rack_id INT NOT NULL,
            capacity INT NOT NULL DEFAULT 0,
            FOREIGN KEY (rack_id) REFERENCES rack(rack_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS master (
            master_id BIGINT PRIMARY KEY,
            row_id INT NOT NULL,
            rack_id INT NOT NULL,
            shelf_id INT NOT NULL,
            FOREIGN KEY (row_id) REFERENCES row_table(row_id),
            FOREIGN KEY (rack_id) REFERENCES rack(rack_id),
            FOREIGN KEY (shelf_id) REFERENCES shelf(shelf_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(150),
            publisher VARCHAR(150),
            category VARCHAR(100),
            quantity INT NOT NULL DEFAULT 0,
            available INT NOT NULL DEFAULT 0,
            master_id BIGINT NOT NULL,
            FOREIGN KEY (master_id) REFERENCES master(master_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(150),
            role VARCHAR(50),
            doj DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            book_id INT NOT NULL,
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            status VARCHAR(20) NOT NULL DEFAULT 'Issued',
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
        """
    ]

    try:
        for query in table_queries:
            cursor.execute(query)
        connection.commit()
        print("All tables verified/created successfully")
    except Exception as e:
        connection.rollback()
        print("Error creating tables :", e)
        raise
