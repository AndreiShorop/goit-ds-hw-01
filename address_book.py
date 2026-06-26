from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Phone number must contain exactly 10 digits: {value}")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value
    

# Saving addressbook to file

def save_data(book,filename = 'address_book.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)

def load_data(filename = 'address_book.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
            

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self,birthday):
        self.birthday = Birthday(birthday)


    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        birthday = str(self.birthday) if self.birthday != None else "N/A"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []
        for record in self.data.values():
            if not record.birthday:
                continue
            bday = datetime.strptime(str(record.birthday.value), "%d.%m.%Y").date()
            bday_this_year = bday.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)
            delta = (bday_this_year - today).days
            if 0 <= delta <= 7:
                if bday_this_year.weekday() == 5:
                    bday_this_year += timedelta(days=2)
                elif bday_this_year.weekday() == 6:
                    bday_this_year += timedelta(days=1)
                result.append({"name": record.name.value, "birthday": bday_this_year.strftime("%d.%m.%Y")})
        return result

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


