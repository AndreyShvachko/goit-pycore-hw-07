from collections import UserDict 
import re 
from datetime import datetime, timedelta
 
class Field: 
    def __init__(self, value): 
        self.value = value 
 
    def __str__(self): 
        return str(self.value) 
 
class Name(Field): 
    pass 
 
class Phone(Field): 
    def __init__(self, value): 
        if not re.fullmatch(r'\d{10}', value): 
            raise ValueError("Phone number must contain exactly 10 digits.") 
        super().__init__(value) 

class Record: 
    def __init__(self, name): 
        self.name = Name(name) 
        self.phones = [] 
        self.birthday = None
 
    def add_phone(self, phone): 
        self.phones.append(Phone(phone)) 
 
    def remove_phone(self, phone): 
        self.phones = [p for p in self.phones if p.value != phone] 
 
    def edit_phone(self, old_phone, new_phone): 
        for p in self.phones: 
            if p.value == old_phone: 
                self.phones.remove(p) 
                self.phones.append(Phone(new_phone)) 
                return 
 
    def find_phone(self, phone): 
        for p in self.phones: 
            if p.value == phone: 
                return p 
        return None 
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
 
    def __str__(self): 
        phones = ';'.join(p.value for p in self.phones)
        birthday = str(self.birthday) if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" 
 
class AddressBook(UserDict): 
    def add_record(self, record): 
        self.data[record.name.value] = record 
 
    def find(self, name): 
        return self.data.get(name, None) 
 
    def delete(self, name): 
        if name in self.data: 
            del self.data[name] 

    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = datetime.now()
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if today <= next_birthday <= today + timedelta(days=days):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    

def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except (IndexError, ValueError) as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        return wrapper
    
@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
       record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"{record.name.value}: {','.join(p.value for p in record.phones)}"
    return "Contact not found."

@input_error
def show_all(args, book):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{record.name.value}: {record.birthday}"
        return "Birthday not set."
    return "Contact not found."   

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(str(record) for record in upcoming)

def parse_input(user_input):
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to assistance bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
   
if __name__ == "__main__":   
    
    main()
