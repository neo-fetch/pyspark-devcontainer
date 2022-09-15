# Create a library management system with the following objects:
# 1. Book
# 2. Student
# 3. Staff
# 4. Author

# This is the main program that will run the library management system
# It will be a menu driven program that will allow the user to select
# Import the classes from the other files


import uuid
from book import Books
import student
import staff
import author
import os

os.system("cls" if os.name == "nt" else "clear")
import sys
import time
import numpy as np
import pandas as pd
from tabulate import tabulate
import shutil
from tqdm import tqdm

# We use sql from pyspark to create a dataframe
import pyspark

# Create a list of books that can be issued
def init():
    # Data format for the db is as follows:
    # [Book Name, Author, Total Copies, Available Copies]
    # The data is then saved to a file (bookdb.csv)
    # Where Total copies are at most 10

    books = pd.read_html("https://www.careerpower.in/books-and-authors.html")
    j = 0
    df_book = pd.DataFrame(columns=["Book Name", "Author", "Year", "Book ID"])
    df_book.to_csv("bookdb.csv", index=False)
    df_status = pd.DataFrame(columns=["Book ID", "Available Status", "Issued Status"])
    df_status.to_csv("statusdb.csv", index=False)
    df_student = pd.DataFrame(
        columns=["Student ID", "Book ID", "Issue Date", "Return Date"]
    )
    df_student.to_csv("studentdb.csv", index=False)
    for book in books:
        # putting some lag for better readability
        # time.sleep(0.1)
        # print(f'Year: {2022 - i} \nBooks:')
        # print(*[f'{book[0][1+i]}, {book[1][1+i]}\n' for i in range(len(book[0][1])-1)])
        # Save the data to a file: bookdb.csv in the format
        # [Book Name, Author, Year, Book ID]
        # Store data in a dataframe after initializing it
        for i in range(len(book[0][1:])):
            df_book.loc[i] = [
                book[0][1 + i].lower(),
                book[1][1 + i].lower(),
                2022 - j,
                uuid.uuid4(),
            ]
        df_book.to_csv("bookdb.csv", mode="a", header=False, index=False)

        j += 1
        # Save some data into another "status.csv" file to see the status of the books available and issued
        # [Book ID, Available Status, Issued Status]
        for i in range(len(book[0][1:])):
            df_status.loc[i] = [
                df_book["Book ID"][i],
                10,
                0,
            ]  # Denoting 10 copies available and 0 copies issued
        df_status.to_csv("statusdb.csv", mode="a", header=False, index=False)

    # Create a dataframe for the student issue history
    # [Student ID, Book ID, Issue Date, Return Date]
    df_student.to_csv("studentdb.csv", mode="a", header=False, index=False)
    # print all the three dataframes in an organized manner
    terminal_columns = shutil.get_terminal_size().columns
    time.sleep(1)
    print(" +-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+".center(terminal_columns))
    print(" |I| |N| |I| |T|   |C| |O| |M| |P| |L| |E| |T| |E|".center(terminal_columns))
    print(" +-+ +-+ +-+ +-+   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+".center(terminal_columns))
    time.sleep(1)
    choice = input("Do you want to see the data? (y/n): ")
    while choice != "y" and choice != "n":
        choice = input("Invalid choice. Do you want to see the data? (y/n): ")
    if choice == "y":
        print(tabulate(pd.read_csv('bookdb.csv'), headers="keys", tablefmt="psql"))
        print(tabulate(pd.read_csv('statusdb.csv'), headers="keys", tablefmt="psql"))
        print(tabulate(pd.read_csv('studentdb.csv'), headers="keys", tablefmt="psql"))
        choice = input("Continue to the main menu? (y/n): ")
        while choice != "y" and choice != "n":
            choice = input("Invalid choice. Continue to the main menu? (y/n): ")
        if choice == "y":
            os.system("cls" if os.name == "nt" else "clear")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            print("Thank you for using the library management system!")
            os._exit(0)

    else:
        print("Exiting initialization")
        # Sleep for 2 seconds
        time.sleep(0.5)
        os.execl(sys.executable, sys.executable, *sys.argv)  # Restart the program


def run():
    print("Welcome to Library Operations!")
    print("Please select an option from the menu below: (Default is 1)")
    print("1. Book Operations")
    print("2. Student Data")
    print("3. Staff/Admin Operations")
    print("4. Author Data")
    print("5. Go to the main menu")
    choice = input("\n\nEnter your choice: \n")
    if choice == "1" or choice == "":
        os.system("cls" if os.name == "nt" else "clear")
        # Just in case you're on Windows
        Books("bookdb.csv", "statusdb.csv", "studentdb.csv")

    elif choice == "2":
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        print("Student Data subroutines")
    elif choice == "3":
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        print("Staff/Admin Operations subroutines")
    elif choice == "4":
        os.system("cls" if os.name == "nt" else "clear")
        print("Author Data subroutines")
    elif choice == "5":
        os.system("cls" if os.name == "nt" else "clear")
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        print("\n\nInvalid choice! Please try again.")
        # Sleep for 2 seconds
        time.sleep(2)
        run()


if __name__ == "__main__":
    # Run the interactive shell after init
    print("Welcome to the Library Management System!")
    print("Please select an option from the menu below: (Default is 1)")
    print("1. Library Operations")
    print("2. Reinitialize the Library")
    print("3. Exit")
    choice = input("\n\nEnter your choice: \n")
    if choice == "1" or choice == "":
        os.system("cls" if os.name == "nt" else "clear")
        # Just in case you're on Windows
        # Check if bookdb.csv is empty. If it is, then initialize the library
        if os.stat("bookdb.csv").st_size == 0:
            print(
                "It seems that the library is not initialized. Initializing the library with default data."
            )
            time.sleep(1)
            init()

        # Fake progress bar:
        
        for i in tqdm(range(100), ascii=" ▖▘▝▗▚▞█", desc="Loading the library data microservice"):
            time.sleep(0.01)
        run()
    elif choice == "2":
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        init()
    elif choice == "3":
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        print("\n\nThank you for using the Library Management System!")
        os._exit(0)
    else:
        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Just in case you're on Windows
        print("\n\nInvalid choice! Please try again.")
        # Sleep for 2 seconds
        time.sleep(2)
        # Clear the screen
        os.execl(sys.executable, sys.executable, *sys.argv)
