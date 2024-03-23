from collections import UserDict
from datetime import datetime

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
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
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
                birthday = user.birthday
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    pass
                else:
                    delta_days = (birthday_this_year - today).days
                    if delta_days < 7:
                        if (birthday_this_year.strftime("%A") == "Saturday" or birthday_this_year.strftime("%A") == "Sunday") and today.strftime("%A") == "Monday":
                            if res.get("next_Monday") is None:
                                res["next_Monday"]=[name]
                            else:
                                res["next_Monday"].append(name)
                        elif (birthday_this_year.strftime("%A") == "Saturday" or birthday_this_year.strftime("%A") == "Sunday") and today.strftime("%A") != "Monday":
                            print("M")
                            if res.get("Monday") is None:
                                res["Monday"]=[name]
                            else:
                                res["Monday"].append(name)
                        else:
                            if res.get(birthday_this_year.strftime("%A")) is None:
                                res[birthday_this_year.strftime("%A")]=[name]
                            else:
                                res[birthday_this_year.strftime("%A")].append(name)
            else:
                pass
    
        for k, v in res.items():
            j_v = ", ".join(v)
            print(f"{k}: {j_v}")
    
