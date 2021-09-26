# import models file
from models import (Base, session, Book, engine)
import datetime
import csv
import time


# main menu add - searc - analysis - exit- view
def menu():
    while True:
        print('''
        \nProgramming Books
        \r1) Add book
        \r2) View Book
        \r3) Search for books
        \r4) Book Analysis
        \r5) Exit ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''\rPlease choose from one of the options above.
            \rA number from 1 to 5
            \rPress Enter to try again''')

            
def submenu():
    while True:
        print('''
        \n1) Edit book
        \r2) Delete Book
        \r3) Return to main menu.''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''\rPlease choose from one of the options above.
            \rA number from 1 to 3
            \rPress Enter to try again''')
    


    
def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October','November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]))+1
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
                \n*****Date Error*****
                \rThe date formate should include a valid (Month Day, Year) from the past
                \rEx: March 25, 2015
                \rPress Enter to try again
                \r********************''')
        return
    else:
        return return_date
    

    
def clean_price(price_str):
    try:
        price_float =  float(price_str)
        return int(price_float * 100)
    except ValueError:
        input('''
                \n*****Price Error*****
                \rThe Price should be a number without a currency symbol
                \rEx: 10.99
                \rPress Enter to try again
                \r********************''')
    else:
        return int(price_float * 100)
        


def clean_id(id_str, option):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
                \n*****ID Error*****
                \rThe ID should be a number.
                \rPress Enter to try again
                \r********************''')
        return
    else:
        if book_id in option:
            return book_id
        else:
            input(f'''
                \n*****ID Error*****
                \rOptions: {option}
                \rPress Enter to try again
                \r********************''')
            return

def edit_check(column_name, current_value):
    print(f'\n***** Edit {column_name} *****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'Current Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')
        
        
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    
    else:
        return input('What would you like to change the value to? ')


    
def add_csv():
    
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]                    
                date = clean_date(row[2])
                price =  clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
                time.sleep(1.5)
                    
                    
                    
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add books
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (EX: October 1, 2015): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
                    
            price_error = True
            while price_error:   
                price = input('Price (Ex: 29.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book Added')
        
        
        elif choice == '2':
            # view books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} ')
            input('Press Enter to return to the main menu.')    
        elif choice == '3':
            # search for books
            id_option = []
            for book in session.query(Book):
                id_option.append(book.id)
                
            id_error = True
            while id_error:
                book_id = input(f'''
                \nID option: {id_option}
                \rBook ID: ''')
                book_id = clean_id(book_id, id_option)
                if type(book_id) == int:
                    id_error = False
                
            the_book = session.query(Book).filter(Book.id == book_id).first()
            print(f'''
                    \n{the_book.title} by {the_book.author} 
                    \rPublished: {the_book.published_date}
                    \rPrice: ${the_book.price / 100}''')
            sub_choice = submenu()
            if sub_choice == '1':
                # edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print("Book Updated")
                time.sleep(1.5)
                
            elif sub_choice == '2':
                session.delete(the_book)
                session.commit()
                print("Book Deleted")
                time.sleep(1.5)
                           
                           
        elif choice == '4':
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
            print(f'''
                \n***** Book Analysis *****
                \rOldest Book: {oldest_book}
                \rNewest Book: {newest_book}
                \rBooks having python in title: {python_books}
                \rTotal Books: {total_books}
                \r**************************''')
            input("Press Enter to return to the main menu.")
            
        else:
            print("Good Bye")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()