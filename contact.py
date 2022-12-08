# Import necessary modules
import pymongo
import csv
from typing import Any
# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database and collection
db = client["contact_manager"]
contacts = db["contacts"]

def add_contact(name: str, email:str, phone: int):

  '''
  Helper function: Adds the given contact details to the connected database.
  Inputs: name (str) -> Name of the contact,
          email(str) -> Email of the contact,
          phone(int) -> Phone number of the contact
  returns: None
  '''

  contact = {
    "name": name,
    "email": email,
    "phone": phone
  }
  contacts.insert_one(contact)
  print('#'*60)
  print("Contact added successfully!")
  print('#'*60)

def search_contact(query: str):

  '''
  Helper function: Searches the database for the given query in either name or email field.
  Inputs: query (str) -> Name or email of the contact,
  returns: None
  '''

  search_results = contacts.find({"$or": [{"name": query}, {"email": query}]})
  if search_results.count() > 0:
    print("Search results:")
    for result in search_results:
      print(result["name"] + " - " + result["email"] + " - " + result["phone"])
  else:
    print('#'*60)
    print("No results found for the given query.")
    print('#'*60)

def update_contact(name: str, email:str, phone: int):

  '''
  Helper function: Updates email and phone  number of the given person based on their name.
  Inputs: name (str) -> Name of the contact,
          email(str) -> Email of the contact,
          phone(int) -> Phone number of the contact
  returns: None
  '''

  update_results = contacts.update_one({"name": name}, {"$set": {"email": email, "phone": phone}})
  if update_results.modified_count > 0:
    print('#'*60)
    print("Contact updated successfully!")
    print('#'*60)

  else:
    print('#'*60)
    print("No contact found with the given name.")
    print('#'*60)


# Function to delete a contact
def delete_contact(name: str):

  '''
  Helper function: Deletes the given contacts based on the name
  Inputs: name (str) -> Name of the contact,
  returns: None
  '''

  delete_results = contacts.delete_one({"name": name})
  if delete_results.deleted_count > 0:
    print('#'*60)
    print("Contact deleted successfully!")
    print('#'*60)
  else:
    print('#'*60)
    print("No contact found with the given name.")
    print('#'*60)

# Function to import contacts from a CSV file
def import_contacts(file_path: str):

  '''
  Helper function: Opens the file from the given file_path, handles file missing exceptions and adds extensions. 
  Quits the program on second exception.

  Inputs: file_path (str) -> path of the input file,
  returns: None
  '''

  try:
    with open(file_path,'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for row in csv_reader:
        add_contact(row["name"], row["email"], row["phone"])
    print('#'*60)
    print("Contacts imported successfully!")
    print('#'*60)
  except FileNotFoundError:
    try:
      file_path+='.csv'
      with open(file_path,'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
          add_contact(row["name"], row["email"], row["phone"])
      print('#'*60)
      print("Contacts imported successfully!")
      print('#'*60)    
    except FileNotFoundError:
      print('\n'+'?'*80)
      print('Given File Couldn\'nt be found. Please make sure the given directory is correct. \nRestarting the program..')
      print('?'*80+'\n')

# Function to export contacts to a CSV file
def export_contacts(file_path: str):

  '''
  Helper function: Opens the file from the given file_path, handles permission denied and improper path exceptions and adds extensions. 
  Quits the program on second exception.

  Inputs: file_path (str) -> path of the output file,
  returns: None
  '''

  try:
    with open(file_path, "w") as csv_file:
      fieldnames = ["name", "email", "phone"]
      csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      csv_writer.writeheader()
      all_contacts = contacts.find()
      for contact in all_contacts:
        csv_writer.writerow({"name": contact["name"], "email": contact["email"], "phone": contact["phone"]})
    print('#'*60)
    print("Contacts exported successfully!")
    print('#'*60)

  except Exception as e:
    print('The following error occured while opening the file. \n' + str(e))
    print('Retrying to open the file with added .csv extension..')

    try:
      file_path+='.csv'
      with open(file_path, "w") as csv_file:
        fieldnames = ["name", "email", "phone"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        all_contacts = contacts.find()
        for contact in all_contacts:
          csv_writer.writerow({"name": contact["name"], "email": contact["email"], "phone": contact["phone"]})
      print('#'*60)
      print("Contacts exported successfully!")
      print('#'*60)

    except Exception as e:
      print("Permission Denied!!")
      print(e)
      print('?'*15+ ' Please give a valid filepath that has write permission!' + '?' * 15)

# Sample usage
# add_contact("Abhishek Khanal", "abhishekkhanal@email.com", "202-912-3345")
# search_contact("Abhishek Khanal")
# update_contact("Abhsihek Khanal", "abhishekkhanal@gmail.com", "202-765-4321")


def print_all_contacts():

  '''
  Helper function: prints all contacts in the given database.  
  returns: None
  '''

  all_contacts = contacts.find()
  if all_contacts.count() > 0:
    print("All contacts:")
    for contact in all_contacts:
      print(contact["name"] + " - " + contact["email"] + " - " + contact["phone"])
  else:
    print("No contacts found.")

def check_int_type(inp: Any) -> int:

    '''
    Helper function:
    Converts the given input to integer if possible if, else returns exception.
    Parameter: inp -> input
    Returns inp as int or exception
    '''

    try:
        inp = int(inp)
        return inp
    except Exception as exception:
        print('\n'+'#'*100)
        print('Conversion Error. The following exception was thrown: ' + str(exception))
        print("Invalid option, please only enter integers and kindly omit other details. Restarting the program....")
        print('#'*100+'\n')
        return 0



# Main function
def main():
  '''
  Displays program header and runs the script based on user's input
  '''
  print('*'*80)
  print("Welcome to my Contact Management System.")

  while True:
    print('*'*80)
    print('Please choose one of the following options!')
    print('*'*100)

    print('''Option 1. Add a Contact \t Option 2. Search for a contact \t Option 3 Update a contact
    \nOption 4. Delete a Contact \t Option 5. Import contacts froma \t option 6. Export contacts to a CSV file
    \nOption 7. Print all contacts \t Option 0. Exit the program
    ''')
    print('-'*100)

    user_input = input('Enter your option here and press enter. ')

    if user_input == "1":
      name = input("Enter contact name: ")
      email = input("Enter contact email: ")
      phone = input("Enter contact phone: ")
      phone_int = check_int_type(phone)
      if phone_int:
        add_contact(name, email, phone_int)

    elif user_input == "2":
      query = input("Enter name or email to search: ")
      search_contact(query)

    elif user_input == "3":
      print('Please enter the same Name while entering either a new email or phone number.')
      name = input("Enter contact name: ")
      email = input("Enter contact email: ")
      phone = input("Enter contact phone: ")
      phone_int = check_int_type(phone)
      if phone_int:
        update_contact(name, email, phone_int)

    elif user_input == "4":
      name = input("Enter contact name: ")
      delete_contact(name)

    elif user_input == "5":
      file_path = input("Enter CSV file path: ")

      import_contacts(file_path)
    elif user_input == "6":
      file_path = input("Enter CSV file path: ")
      export_contacts(file_path)

    elif user_input == "7":
      print_all_contacts()

    elif user_input == "0":
      print('\nThank you for using this script. This program was made by .')
      break

    else:
      print("\nPlease choose a valid integer between 0 and 7. Restarting the program...")

if __name__ == "__main__":
  main()
