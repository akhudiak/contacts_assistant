from collections import UserDict
from datetime import datetime
from string import digits

from exceptions import IncorrectPhone, IncorrectBirthday


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, name):
        self.data.pop(name)

    def search_record(self, args):

        name = args[0]

        if name not in self.data:
            return f"There is no contact with the name {name}"
        
        phones = [phone.value for phone in self.data[name].phones]

        if len(args) > 1:
            for phone in args[1:]:
                if phone not in phones:
                    return f"There is no contact {name} with the phone {phone}"

        phones = "; ".join(phones)

        return f"{name}: {phones}"
    
    def iterator(self, n):

        start_point = 0
        list_data = list(self.data)

        while True:

            page = list_data[start_point:start_point + n]

            if not page:
                break

            start_point += n

            yield page


class Record:

    def __init__(self, name, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def del_phone(self, phone):
        self.phones.remove(phone)

    def change_phones(self, old_phone, new_phone):
        
        for phone in self.phones:
            if phone.value == old_phone:
                old_phone = phone

        if isinstance(old_phone, str):
            return f"There is no such phone {old_phone} in the contact with name {self.name.value}"

        index = self.phones.index(old_phone)
        self.phones.pop(index)
        self.phones.insert(index, new_phone)

        return "Phones changed successfully"

    def days_to_birthday(self):

        if not self.birthday.value: # Подумати чи потрібно тут .value
            return "Birthday is not specified"
        
        current_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        current_birthday = datetime(current_date.year, self.birthday.value.month, self.birthday.value.day)
        
        if current_date > current_birthday:
            next_birthday = datetime(current_date.year + 1, current_birthday.month, current_birthday.day)
        else:
            next_birthday = current_birthday

        days_to_next_birthday = (next_birthday - current_date).days
        return f"There is {days_to_next_birthday} days to the next birthday of {self.name.value}"


class Field:

    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):

    available_chars = digits + "+-() "

    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):

        for ch in value:
            if ch not in self.available_chars:
                raise IncorrectPhone
            
        self.__value = value


class Birthday(Field):
    
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):

        try:
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise IncorrectBirthday