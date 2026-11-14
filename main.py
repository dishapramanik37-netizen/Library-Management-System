from database import connect_database, create_tables
from mysql.connector import Error
from database import connect_database, create_tables

def add_book():
    connection = connect_database()

    if connection:
        try:
            cursor = connection.cursor()

            title = input("Enter book title: ")
            author = input("Enter author name: ")
            quantity = int(input("Enter book quantity: "))

            query = """
            INSERT INTO books (title, author, quantity)
            VALUES (%s, %s, %s)
            """

            values = (title, author, quantity)

            cursor.execute(query, values)
            connection.commit()

            print("Book added successfully!")

        except ValueError:
            print("Please enter a valid number for quantity.")

        except Error as e:
            print("Error adding book:", e)

        finally:
            cursor.close()
            connection.close()


def view_books():
    connection = connect_database()

    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()

            print("\n========== BOOK LIST ==========")

            if books:
                for book in books:
                    print("Book ID:", book[0])
                    print("Title:", book[1])
                    print("Author:", book[2])
                    print("Quantity:", book[3])
                    print("-----------------------------")
            else:
                print("No books found in the library.")

        except Error as e:
            print("Error displaying books:", e)

        finally:
            cursor.close()
            connection.close()


def search_book():
    connection = connect_database()

    if connection:
        try:
            cursor = connection.cursor()

            title = input("Enter book title to search: ")

            query = """
            SELECT book_id, title, author, quantity
            FROM books
            WHERE title LIKE %s
            """
            cursor.execute(query, ("%" + title + "%",))

            books = cursor.fetchall()

            if books:
                print("\n========== SEARCH RESULTS ==========")

                for book in books:
                    print("Book ID:", book[0])
                    print("Title:", book[1])
                    print("Author:", book[2])
                    print("Quantity:", book[3])
                    print("-----------------------------")
            else:
                print("Book not found!")

        except Error as e:
            print("Error searching book:", e)

        finally:
            cursor.close()
            connection.close()

def register_student():
    connection = connect_database()

    if connection:
        cursor = None

        try:
            cursor = connection.cursor()

            name = input("Enter student name: ")
            email = input("Enter student email: ")
            phone = input("Enter student phone: ")

            query = """
            INSERT INTO students (name, email, phone)
            VALUES (%s, %s, %s)
            """

            values = (name, email, phone)

            cursor.execute(query, values)
            connection.commit()

            print("Student registered successfully!")

        except Error as e:
            print("Error registering student:", e)

        finally:
            if cursor:
                cursor.close()
            connection.close()
   

def view_students():
    connection = connect_database()

    if connection:
        try:
            cursor = connection.cursor()

            query = "SELECT * FROM students"
            cursor.execute(query)

            students = cursor.fetchall()

            print("\n========== REGISTERED STUDENTS ==========")

            if not students:
                print("No students registered yet.")

            else:
                for student in students:
                    print("Student ID:", student[0])
                    print("Name:", student[1])
                    print("Email:", student[2])
                    print("Phone:", student[3])
                    print("-----------------------------")

        except Error as e:
            print("Error viewing students:", e)

        finally:
            cursor.close()
            connection.close()

def issue_book():
    connection = connect_database()

    if connection:
        cursor = None

        try:
            cursor = connection.cursor()

            book_id = int(input("Enter book ID: "))
            student_id = int(input("Enter student ID: "))

            # Check whether the book exists
            query = """
            SELECT quantity FROM books
            WHERE book_id = %s
            """
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()

            if book is None:
                print("Book not found!")

            elif book[0] <= 0:
                print("Book is not available!")

            else:
                # Check whether the student exists
                query = """
                SELECT * FROM students
                WHERE student_id = %s
                """
                cursor.execute(query, (student_id,))
                student = cursor.fetchone()

                if student is None:
                    print("Student not found!")

                else:
                    # Insert issue record
                    query = """
                    INSERT INTO issued_books
                    (book_id, student_id, issue_date)
                    VALUES (%s, %s, CURDATE())
                    """
                    cursor.execute(query, (book_id, student_id))

                    # Reduce book quantity
                    query = """
                    UPDATE books
                    SET quantity = quantity - 1
                    WHERE book_id = %s
                    """
                    cursor.execute(query, (book_id,))

                    connection.commit()

                    print("Book issued successfully!")

        except ValueError:
            print("Please enter valid numeric IDs.")

        except Error as e:
            connection.rollback()
            print("Error issuing book:", e)

        finally:
            if cursor:
                cursor.close()
            connection.close()


def return_book():
    connection = connect_database()

    if connection:
        cursor = None

        try:
            cursor = connection.cursor()

            book_id = int(input("Enter book ID: "))
            student_id = int(input("Enter student ID: "))

            # Check whether this book was issued to this student
            query = """
            SELECT * FROM issued_books
            WHERE book_id = %s AND student_id = %s
            """
            cursor.execute(query, (book_id, student_id))
            issued_book = cursor.fetchone()

            if issued_book is None:
                print("No issued record found!")

            else:
                # Delete the issue record
                query = """
                DELETE FROM issued_books
                WHERE book_id = %s AND student_id = %s
                """
                cursor.execute(query, (book_id, student_id))

                # Increase book quantity
                query = """
                UPDATE books
                SET quantity = quantity + 1
                WHERE book_id = %s
                """
                cursor.execute(query, (book_id,))

                connection.commit()

                print("Book returned successfully!")

        except ValueError:
            print("Please enter valid numeric IDs.")

        except Error as e:
            connection.rollback()
            print("Error returning book:", e)

        finally:
            if cursor:
                cursor.close()
            connection.close()


def view_issued_books():
    connection = connect_database()

    if connection:
        cursor = None

        try:
            cursor = connection.cursor()

            query = """
            SELECT 
                issued_books.book_id,
                books.title,
                issued_books.student_id,
                students.name,
                issued_books.issue_date
            FROM issued_books
            JOIN books
                ON issued_books.book_id = books.book_id
            JOIN students
                ON issued_books.student_id = students.student_id
            """

            cursor.execute(query)
            records = cursor.fetchall()

            if not records:
                print("No books have been issued yet.")

            else:
                print("\n========== ISSUED BOOKS ==========")

                for record in records:
                    print("--------------------------------")
                    print("Book ID:", record[0])
                    print("Book Title:", record[1])
                    print("Student ID:", record[2])
                    print("Student Name:", record[3])
                    print("Issue Date:", record[4])

        except Error as e:
            print("Error displaying issued books:", e)

        finally:
            if cursor:
                cursor.close()
            connection.close()

def main_menu():
    while True:
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Register Student")
        print("5. View Students")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. View Issued Books")
        print("9. Exit")

        
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            register_student()

        elif choice == "5":
            view_students()

        elif choice == "6":
            issue_book()

        elif choice == "7":
            return_book()

        elif choice == "8":
            view_issued_books()

        elif choice == "9":
            print("Thank you for using Library Management System!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 9.")


if __name__ == "__main__":
    create_tables()
    main_menu()
