from collections import UserDict

class NumberIsNotTenDigit(Exception):
    pass

class NumberIsNotNumeric(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

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