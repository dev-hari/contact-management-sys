# Import necessary modules
import pymongo
import csv

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database and collection
db = client["contact_manager"]
contacts = db["contacts"]

# Function to add a new contact
def add_contact(name, email, phone):
  contact = {
    "name": name,
    "email": email,
    "phone": phone
  }
  contacts.insert_one(contact)
  print("Contact added successfully!")

# Function to search for a contact by name or email
def search_contact(query):
  search_results = contacts.find({"$or": [{"name": query}, {"email": query}]})
  if search_results.count() > 0:
    print("Search results:")
    for result in search_results:
      print(result["name"] + " - " + result["email"] + " - " + result["phone"])
  else:
    print("No results found for the given query.")

# Function to update a contact's information
def update_contact(name, email, phone):
  update_results = contacts.update_one({"name": name}, {"$set": {"email": email, "phone": phone}})
  if update_results.modified_count > 0:
    print("Contact updated successfully!")
  else:
    print("No contact found with the given name.")

# Function to delete a contact
def delete_contact(name):
  delete_results = contacts.delete_one({"name": name})
  if delete_results.deleted_count > 0:
    print("Contact deleted successfully!")
  else:
    print("No contact found with the given name.")

# Function to import contacts from a CSV file
def import_contacts(file_path):
  with open(file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      add_contact(row["name"], row["email"], row["phone"])
  print("Contacts imported successfully!")

# Function to export contacts to a CSV file
def export_contacts(file_path):
  import csv
  with open(file_path, "w") as csv_file:
    fieldnames = ["name", "email", "phone"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    all_contacts = contacts.find()
    for contact in all_contacts:
      csv_writer.writerow({"name": contact["name"], "email": contact["email"], "phone": contact["phone"]})
  print("Contacts exported successfully!")

# Sample usage
add_contact("Abhishek Khanal", "abhishekkhanal@email.com", "202-912-3345")
search_contact("Abhishek Khanal")
update_contact("Abhsihek Khanal", "abhishekkhanal@gmail.com", "202-765-4321")


# Function to print all contacts
def print_all_contacts():
  all_contacts = contacts.find()
  if all_contacts.count() > 0:
    print("All contacts:")
    for contact in all_contacts:
      print(contact["name"] + " - " + contact["email"] + " - " + contact["phone"])
  else:
    print("No contacts found.")

# Function to handle user input
def handle_user_input():
  while True:
    print("Enter 1 to add a contact")
    print("Enter 2 to search for a contact")
    print("Enter 3 to update a contact")
    print("Enter 4 to delete a contact")
    print("Enter 5 to import contacts from a CSV file")
    print("Enter 6 to export contacts to a CSV file")
    print("Enter 7 to print all contacts")
    print("Enter 0 to exit")
    user_input = input()

    if user_input == "1":
      name = input("Enter contact name: ")
      email = input("Enter contact email: ")
      phone = input("Enter contact phone: ")
      add_contact(name, email, phone)
    elif user_input == "2":
      query = input("Enter name or email to search: ")
      search_contact(query)
    elif user_input == "3":
      name = input("Enter contact name: ")
      email = input("Enter contact email: ")
      phone = input("Enter contact phone: ")
      update_contact(name, email, phone)
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
      break

# Main function
def main():
  handle_user_input()

if __name__ == "__main__":
  main()
