import mysql.connector
from datetime import datetime,date
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER
class Book:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASS,
            database = DB_NAME
        )

        if self.connection.is_connected:
            print("connected to database successfully")
            self.cursor = self.connection.cursor()
            self.cursor.execute("show tables;")
            results = self.cursor.fetchall()
            for row in results:
                print(row)

        create_table_query = """
            CREATE TABLE IF NOT EXISTS books (
                    book_id INT AUTO_INCREMENT PRIMARY KEY,
                    book_name VARCHAR(255) NOT NULL,
                    author VARCHAR(255),
                    total_book_pages INT NOT NULL,
                    days INT NOT NULL,
                    last_read_date DATE,
                    pages_read INT NOT NULL DEFAULT 0,
                    days_remaining INT,
                    pages_remaining INT,
                    pages_per_day FLOAT
                );
                """

        self.cursor.execute(create_table_query)
        self.connection.commit()

        print("✅ Table 'books' created successfully!")
    def add_book(self):
        while True:    
            print("1.add_book\n2.update_progress\n3.view_progress\n4.exit")
            choice = int(input("Enter your choice:- "))
            if choice == 1:

                book_name = input("Enter book name:- ")
                author = input("Enter author name:- ")
                total_book_pages = int(input("Enter no. of book pages:- "))
                days = int(input("Enter the no. of days you want to finish this book:- "))
                last_read_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                pages_read = int(input("Enter pages you read today:- "))
                days_remaining = days - (date.today() - last_read_date).days
                pages_reamining = total_book_pages - pages_read
                pages_per_day = round(pages_reamining/days_remaining,2)
                print(book_name,author,total_book_pages,days,last_read_date,pages_read,days_remaining,pages_reamining,pages_per_day)

                sql = """INSERT INTO books (book_name,author,total_book_pages,days,last_read_date,pages_read,
                days_remaining,pages_remaining,pages_per_day)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (book_name,author,total_book_pages,days,last_read_date,pages_read,days_remaining,pages_reamining,pages_per_day)
                self.cursor.execute(sql,values)
                self.connection.commit()
                print(self.cursor.rowcount , "Record Inserted.")

            if choice == 2:
                total_pages_read = int(input("Enter pages you read today:- "))
                book_id = int(input("Enter your book id:- "))
                sql = """select days,last_read_date,total_book_pages,pages_read,pages_remaining from books where book_id = %s"""

                self.cursor.execute(sql,(book_id,))
                results = self.cursor.fetchone()
                days, last_read_date, total_book_pages, pages_read, pages_reamining = results
                pages_reamining = total_book_pages - (total_pages_read + pages_read)
                days_remaining = days - (date.today() - last_read_date).days
                pages_per_day = round(pages_reamining/days_remaining,2)
                sql = """update books 
                        set 
                        pages_read = pages_read + %s, days_remaining = %s, pages_remaining = %s, pages_per_day = %s 
                        where book_id = %s"""
                values = (total_pages_read,days_remaining,pages_reamining,pages_per_day,book_id)
                self.cursor.execute(sql,values)
                self.connection.commit()
                print(self.cursor.rowcount,"Record Inserted.")

            if choice == 3:
                book_id = int(input("Enter your book id:- "))
                sql = """select * from books
                        where book_id = %s"""
                # values = (book_id,)
                self.cursor.execute(sql,(book_id,))
                results = self.cursor.fetchall()
                if results:
                    print(results)
                else:
                    print("book not found")        

            if choice == 4:
                break    
        
        
        
book_instance = Book()
book_instance.add_book()
