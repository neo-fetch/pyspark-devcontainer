# import pyspark
# from pyspark.sql import SparkSession
#
# TODO: Reimplement this using pyspark. For now, we will use pandas
#
# ---------------------------------------------------------------------
#
# The book class is used to create a book object and will perform the following:
# Searching book()
# Assign book()
# Book Id
# Is_available_not()
# Book_title
# Author
from secrets import choice
import time
import pandas as pd
from fuzzywuzzy import fuzz
import os


class Books:
    def __init__(self, book_db, status_db, student_db):
        self.book_db = book_db
        self.status_db = status_db
        self.student_db = student_db
        self.book_id = None
        self.book_title = None
        self.author = None
        self.year = None
        self.is_available = None

        # Run the program
        self.run()

    def book_ops(self, book_id=None, student_id=None, action=None):
        print("Welcome to the book operations menu!")
        # If book_id is None, then we need to ask for the book id
        book_id = input("Enter the book ID: ") if book_id is None else book_id
        # If student_id is None, then we need to ask for the student id
        student_id = (
            input("Enter the student ID: ") if student_id is None else student_id
        )
        # If action is None, then we need to ask for the action
        action = (
            input("Enter the action (assign/return): ") if action is None else action
        )

        # Check if the book id is valid

        book_db = pd.read_csv(
            self.book_db
        )  # Format: [Book Name, Author, Year, Book ID]
        valid_book = False
        for bid in book_db["Book ID"]:
            if bid == book_id:
                valid_book = True
                break
        if not valid_book:
            print("Invalid book ID! Returning to main menu...")
            time.sleep(2)
            self.run()
        if action == "assign":
            # Check if the student id is valid if it follows the format: I000[0-9]{4}
            # If it is, then check if the student has already borrowed 3 books
            # If not, then check if the book is available
            # If it is, then assign the book to the student and update the status in status_db
            # If not, then return an error message
            student_db = pd.read_csv(
                self.student_db
            )  # Format: [Student ID, Student Name, Student Class, Student Section, Student Roll No.]
            

    def book_status(self):
        print("Welcome to the book status menu!")
        # Check if the book is available or not
        # If it is, then return True
        # If not, then return False

    def search_book(self, book_title):
        book_db = pd.read_csv(
            self.book_db
        )  # Format: [Book Name, Author, Year, Book ID]

        # Check if there is a 90% match in the book title
        # If there is, then return the book id
        # If not, then return None

        for book, author, year, book_id in zip(
            book_db["Book Name"], book_db["Author"], book_db["Year"], book_db["Book ID"]
        ):
            ratio = fuzz.ratio(book.lower(), f"‘{book_title}’".lower())
            if ratio >= 80:
                print(
                    f"We found a match for ‘{book_title}’ with {book} with an accuracy of {ratio}%."
                )
                choice = input("Is this the book you were looking for? (Y/N): ").lower()
                while choice != "y" and choice != "n":
                    choice = input("Invalid choice! Please try again: ").lower()
                if choice == "y":
                    return book, author, year, book_id
                else:
                    continue

        # If we get here, then we didn't find a match
        os.system("cls" if os.name == "nt" else "clear")
        print("We couldn't find a match for your book. Maybe check the spelling?")
        time.sleep(2)
        return None

    def run(self):
        print("Welcome to Library Operations!")
        print("Please select an option from the menu below: (Default is 1)")
        print("1. Search for a book")
        print("2. Assign a book to a student or return it")
        print("3. Status of a book")
        print("4. Exit to main menu")
        choice = input("\n\nEnter your choice: \n")
        if choice == "1" or choice == "":
            os.system("cls" if os.name == "nt" else "clear")
            # Just in case you're on Windows
            book_title = input("Enter the book title: ")
            book, author, year, book_id = self.search_book(book_title)
            if book is not None:
                print(f"Book ID: {book_id}")
                print(f"Book Title: {book}")
                print(f"Author: {author}")
                print(f"Year: {year}")
                resume = input(
                    "Would you like to assign this book to a student? (Y/N): "
                ).lower()
                while resume != "y" and resume != "n":
                    resume = input("Invalid choice! Please try again: ").lower()
                if resume == "y":
                    print("Assigning book...")
                    time.sleep(2)
                    self.book_ops()
                else:
                    print("Returning to main menu...")
                    time.sleep(2)
                    self.run()
            else:
                self.run()
        elif choice == "2":
            os.system(
                "cls" if os.name == "nt" else "clear"
            )  # Just in case you're on Windows
            self.book_ops()
        elif choice == "3":
            os.system(
                "cls" if os.name == "nt" else "clear"
            )  # Just in case you're on Windows
            self.book_status()
        elif choice == "4":
            os.system("cls" if os.name == "nt" else "clear")
            print("Exiting to main menu...")
            time.sleep(1)
            os.system("python main.py")
        else:
            os.system(
                "cls" if os.name == "nt" else "clear"
            )  # Just in case you're on Windows
            print("\n\nInvalid choice! Please try again.")
            # Sleep for 2 seconds
            time.sleep(2)
            self.run()
