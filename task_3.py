from collections import UserDict
from datetime import datetime

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

class NumberIsNotTenDigit(Exception):
    pass

class NumberIsNotNumeric(Exception):
    pass

class WrongDate(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value) 
        except ValueError:
            raise WrongDate

class Name(Field):
    pass    

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise NumberIsNotTenDigit
        if not value.isnumeric():
            raise NumberIsNotNumeric
        else:
            super().__init__(value)      

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday=None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone added"
    
    def edit_phone(self, old_phone, new_phone):
        n=0
        for i in range(0,len(self.phones)):
            if old_phone == str(self.phones[i].value):    
                n+=1
                self.phones[i]=Phone(new_phone)
        if n == 0:
            print(f"No such phone in {self.name} adress book, unable to edit")

    def find_phone(self, phone_to_search):
        n=0
        for i in range(0,len(self.phones)):
            if phone_to_search == str(self.phones[i].value):    
                n+=1
                return self.phones[i]
        if n == 0:
            print(f"No such phone in {self.name} adress book, unable to find")      

    def remove_phone(self, phone_to_delete):
        n=0
        for i in range(0,len(self.phones)):
            if phone_to_delete == str(self.phones[i].value):    
                n+=1
                del self.phones[i]
        if n == 0:
            print(f"No such phone in {self.name} adress book, unable to delete") 

    def __str__(self):
        print(self.birthday)
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthdays: {self.birthday}"
    
    def add_birthday(self, bday):
        self.birthday=Birthday(bday)

class AddressBook(UserDict):
    data={}
    def add_record(self, record):
        self.data[record.name]=record

    def find(self, name):
        for i in self.data.keys():
            if name == str(i):
                return self.data[i]
            
    def delete(self, name):
        for i in self.data.keys():
            if name == str(i):
                index_to_del=i
        del self.data[index_to_del]

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        res={}
        for user in self.data.values():
            name = user.name
            if user.birthday: 
                birthday = datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    pass
                else:
                    delta_days = (birthday_this_year - today).days
                    if delta_days < 7:
                        if (birthday_this_year.strftime("%A") == "Saturday"
                            or birthday_this_year.strftime("%A") == "Sunday")and today.strftime("%A") == "Monday":
                            if res.get("next_Monday") is None:
                                res["next_Monday"]=[name.value]
                            else:
                                res["next_Monday"].append(name.value)
                        elif (birthday_this_year.strftime("%A") == "Saturday"
                              or birthday_this_year.strftime("%A") == "Sunday") and today.strftime("%A") != "Monday":
                            if res.get("Monday") is None:
                                res["Monday"]=[name.value]
                            else:
                                res["Monday"].append(name.value)
                        else:
                            if res.get(birthday_this_year.strftime("%A")) is None:
                                res[birthday_this_year.strftime("%A")]=[name.value]
                            else:
                                res[birthday_this_year.strftime("%A")].append(name.value)
            else:
                pass
        for k, v in res.items():
            j_v = ", ".join(v)
            print(f"{k}: {j_v}")
    

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                try:
                    name,phone = args
                    record = Record(name)
                    record.add_phone(phone)
                    book.add_record(record)
                except ValueError:
                    print("Wrong input")
                except NumberIsNotNumeric:
                    print("Wrong input, phone number is not a number")
                except NumberIsNotTenDigit:
                    print("Wrong input, phone number is not a ten digit number")
            elif command == "change":
                try:
                    name,new_phone = args
                    record = book.find(name)
                    record.edit_phone(str(record.phones[0]), new_phone)
                except ValueError:
                    print("Wrong input")
            elif command == "phone":
                name = args[0]
                if book.find(name):
                    try:
                        record = book.find(name)
                        print(record.phones[0])
                    except ValueError:
                        print("Wrong input")
                else:
                    print("No such contact")
            elif command == "all":
                if book.data.values():
                    print("All contacts")
                    for i in book.data.values():
                        print(i)
                else:
                    print("Empty contact list")
            elif command == "add-birthday":
                name,bday = args
                if book.find(name):
                    try:
                        
                        record = book.find(name)
                        record.add_birthday(bday)
                    except ValueError:
                        print("Wrong input")
                    except WrongDate:
                        print("Wrong date, use DD.MM.YYYY")
                else:
                    print("No such contact")
            elif command == "show-birthday": 
                try:
                    name = args[0]
                    record = book.find(name)
                    print(record.birthday)
                except ValueError:
                    print("Wrong input")
            elif command == "birthdays":   
                book.get_birthdays_per_week()

            else:
                print("Invalid command.")
        except ValueError:
            print("Invalid command.")

if __name__ == "__main__":
    main()
