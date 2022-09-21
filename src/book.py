#
# TODO: Reimplement this using pyspark. For now, we will use pandas [x]
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

import pyspark
from pyspark.sql import SparkSession
import time
import pandas as pd
from fuzzywuzzy import fuzz
import os
import re
import time
from tqdm import tqdm
from tabulate import tabulate


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
        spark = SparkSession.builder.getOrCreate()  
        
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

        book_db = spark.read.csv(self.book_db, header=True) # Format: [Book Name, Author, Year, Book ID]
        book_db = book_db.withColumn("Year", book_db["Year"].cast("int"))
        status_db = spark.read.csv(self.status_db, header=True) # Format: [Book ID,Available Status,Issued Status]
        status_db = status_db.withColumn("Available Status", status_db["Available Status"].cast("int"))
        status_db = status_db.withColumn("Issued Status", status_db["Issued Status"].cast("int"))
        
        valid_book = False
        for book in book_db.collect():
            if book["Book ID"] == book_id:
                valid_book = True
                break
        # for bid in book_db["Book ID"]:
        #     if bid == book_id:
        #         valid_book = True
        #         break
            # We also need to check if the book is available or not from the status_db
        for status in status_db.collect():
        # for bid, available, issued in zip(
        #     status_db["Book ID"], status_db["Available Status"], status_db["Issued Status"]
        # ):
            if status["Book ID"] == book_id:
                if status["Available Status"] - status["Issued Status"] == 0:
                    print("The book is not available!")
                    valid_book = False
                        
        if not valid_book:
            print("Invalid book ID/ Unavailable! Returning to main menu...")
            time.sleep(2)
            self.run()
        if action == "assign":
            # Check if the student id is valid if it follows the format: I000[0-9]{4}
            if re.match(r"I000[0-9]{4}", student_id):
                # Check if the student id is valid
                student_db = spark.read.csv(self.student_db, header=True) # Format: [Student ID, Book ID, Issue Date, Return Date]
                # If it is, then check if the student has already borrowed 3 books
                valid_student = True
                borrowed_books = 0
                for student in student_db.collect():
                    if student["Student ID"] == student_id:
                        borrowed_books += 1
                        if borrowed_books >= 3:
                            print("Student has already borrowed 3 books!")
                            valid_student = False
                            time.sleep(2)
                            self.run()
                        if student["Book ID"] == book_id:
                            print("Student has already borrowed this book!")
                            valid_student = False
                            time.sleep(2)
                            self.run()
                # If we come this far, then the student has either:
                # 1. Borrowed less than 3 books
                # 2. Not already borrowed this book, removing any chance of a duplicate
                
                # Adding the book to the student's list of borrowed books as [Student ID, Book ID, Today's Date, 15 days from today's date]
                if valid_student:
                    # Add the book to the student's list of borrowed books
                    issue_date = time.strftime("%d/%m/%Y")
                    return_date = time.strftime("%d/%m/%Y", time.localtime(time.time() + 15 * 24 * 60 * 60))
                    new_issue = spark.createDataFrame([[student_id, book_id, issue_date, return_date]], ["Student ID", "Book ID", "Issue Date", "Return Date"])
                    student_db = student_db.union(new_issue)
                    # student_db = student_db.append({"Student ID": student_id, "Book ID": book_id, "Issue Date": issue_date, "Return Date": return_date}, ignore_index=True)
                    # spark.sql(f"INSERT INTO student_db VALUES ({student_id}, {book_id}, {issue_date}, {return_date})")
                    # Update the status_db to reflect the book being issued
                    status_db = status_db.withColumn("Issued Status", status_db["Issued Status"] + 1)\
                        .where(status_db["Book ID"] == book_id)

                    # spark.sql(f"UPDATE status_db SET 'Issued Status' = 'Issued Status' + 1 WHERE 'Book ID' = {book_id}")
                    # for i in range(len(status_db["Book ID"])):
                    #     if status_db["Book ID"][i] == book_id:
                    #         status_db["Issued Status"].loc[i] += 1
                            
                    print("Book assigned successfully!")
                    # print the last 5 rows of the student_db
                    print(student_db.show())
                    # Save the changes back to the csv files
                    student_db.toPandas().to_csv(self.student_db, index=False)
                    status_db.toPandas().to_csv(self.status_db, index=False)
                    # Close spark session
                    spark.stop()
                    os.system("cls" if os.name == "nt" else "clear")
                    # Print student table
                    
                    time.sleep(5)
                    self.run()
    
                
            else:
                print("Invalid student ID! Please try again.")
                time.sleep(2)
                self.book_ops(book_id=book_id, action=action)
            # If not, then check if the book is available
            # If it is, then assign the book to the student and update the status in status_db
            # If not, then return an error message
        elif action == "return":
            if re.match(r"I000[0-9]{4}", student_id):
                # Check if the student id is valid
                student_db = pd.read_csv(
                    self.student_db
                ) # Format: [Student ID, Student Name, Student Class, Student Section, Student Roll No.]
                
                # Scan the books issued by the student from the student_db
                # If the book is found, then remove it from the student_db and update the status_db
                # If not, then return an error message
                
                for student, b_id in zip(student_db["Student ID"], student_db["Book ID"]):
                    if student == student_id and b_id == book_id:
                        # Remove the book from the student_db
                        student_db.drop(student_db.index[student_db["Student ID"] == student_id], inplace=True)
                        # Update the status_db
                        status_db = status_db.withColumn("Issued Status", status_db["Issued Status"] - 1)\
                            .where(status_db["Book ID"] == book_id)
                        # Save the changes
                        student_db.to_csv(self.student_db, index=False)
                        status_db.toPandas().to_csv(self.status_db, index=False)
                        # Close spark session
                        spark.stop()
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Book returned successfully!")
                        print(tabulate(student_db, headers="keys", tablefmt="psql"))
                        time.sleep(2)
                        self.run()
                print("Student has not borrowed this book!")
                time.sleep(2)
                self.run()

            


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

        for book, author, year, book_id in tqdm(zip(
            book_db["Book Name"], book_db["Author"], book_db["Year"], book_db["Book ID"]
        ), total=len(book_db["Book Name"]), ascii=" ▖▘▝▗▚▞█"):
            ratio = fuzz.ratio(book.lower(), f"‘{book_title}’".lower())
            if ratio >= 80:
                os.system("cls" if os.name == "nt" else "clear")
                print(
                    f"We found a match for ‘{book_title}’ with {book} with an accuracy of {ratio}%."
                )
                choice = input("Is this the book you were looking for? (Y/N): ").lower()
                while choice != "y" and choice != "n" and choice != "":
                    choice = input("Invalid choice! Please try again: ").lower()
                if choice == "y" or choice == "":
                    os.system("cls" if os.name == "nt" else "clear")
                    return book, author, year, book_id
                else:
                    continue

        # If we get here, then we didn't find a match
        os.system("cls" if os.name == "nt" else "clear")
        print("We couldn't find a match for your book. Maybe check the spelling?")
        time.sleep(2)
        return None, None, None, None

    def run(self):
        os.system("cls" if os.name == "nt" else "clear")
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
                while resume != "y" and resume != "n" and resume != "":
                    resume = input("Invalid choice! Please try again: ").lower()
                if resume == "y" or resume == "":
                    print("Assigning book...")
                    time.sleep(2)
                    self.book_ops(book_id=book_id)
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
