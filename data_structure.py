from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, name):
        self.data.pop(name)

    def change_record(self, name, phones):
        
        record = self.data[name]
        record.phones = []
        record.ext_phones(phones)

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

    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def ext_phones(self, phones):
        self.phones.extend(phones)

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


class Field:

    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass