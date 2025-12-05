from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime, date
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

@app.route('/')
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    connection.close()
    return render_template("progress.html", books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        author = request.form['author']
        total_book_pages = int(request.form['total_book_pages'])
        days = int(request.form['days'])
        last_read_date = datetime.strptime(request.form['last_read_date'], "%Y-%m-%d").date()
        pages_read = int(request.form['pages_read'])

        days_remaining = days - (date.today() - last_read_date).days
        pages_remaining = total_book_pages - pages_read
        pages_per_day = round(pages_remaining / days_remaining, 2)

        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """INSERT INTO books (book_name,author,total_book_pages,days,last_read_date,pages_read,
                 days_remaining,pages_remaining,pages_per_day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (book_name, author, total_book_pages, days, last_read_date,
                  pages_read, days_remaining, pages_remaining, pages_per_day)
        cursor.execute(sql, values)
        connection.commit()
        connection.close()

        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/update_progress', methods=['GET', 'POST'])
def update_progress():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        total_pages_read = int(request.form['pages_read'])

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT days,last_read_date,total_book_pages,pages_read,pages_remaining
                          FROM books WHERE book_id = %s""", (book_id,))
        result = cursor.fetchone()
        if result:
            days, last_read_date, total_book_pages, pages_read, pages_remaining = result
            if pages_read >= total_book_pages:
                return "🎉 Congratulations! You already finished this book."

            pages_remaining = total_book_pages - (total_pages_read + pages_read)
            days_remaining = days - (date.today() - last_read_date).days
            pages_per_day = round(pages_remaining / days_remaining, 2)

            update_sql = """UPDATE books
                            SET pages_read = pages_read + %s,
                                days_remaining = %s,
                                pages_remaining = %s,
                                pages_per_day = %s
                            WHERE book_id = %s"""
            values = (total_pages_read, days_remaining, pages_remaining, pages_per_day, book_id)
            cursor.execute(update_sql, values)
            connection.commit()
        connection.close()
        return redirect(url_for('home'))
    return render_template('update_progress.html')

if __name__ == '__main__':
    app.run(debug=True)
