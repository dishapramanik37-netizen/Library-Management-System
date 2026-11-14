import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def connect_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("Successfully connected to MySQL!")
            return connection

    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None


def create_tables():
    connection = connect_database()

    if connection:
        try:
            cursor = connection.cursor()

            create_books_table = """
            CREATE TABLE IF NOT EXISTS books (
                book_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100) NOT NULL,
                quantity INT NOT NULL
            )
            """
            cursor.execute(create_books_table)
            print("Books table created successfully!")

            create_students_table = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(15)
            )
            """
            cursor.execute(create_students_table)
            print("Students table created successfully!")

            create_issued_books_table = """
            CREATE TABLE IF NOT EXISTS issued_books (
                issue_id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT NOT NULL,
                student_id INT NOT NULL,
                issue_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """
            cursor.execute(create_issued_books_table)
            print("Issued books table created successfully!")

        except Error as e:
            print("Error creating tables:", e)

        finally:
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    create_tables()


