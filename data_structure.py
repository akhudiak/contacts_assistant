from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, name):
        self.data.pop(name)

    def change_record(self, name, fields):
        
        record = self.data[name]
        record.fields = []
        record.ext_fields(fields)

    def search_record(self, fields):

        name = fields[0]

        if name not in self.data:
            return f"There is no contact with the name {name}"
        
        contact_phones = [field.value for field in self.data[name].fields]

        if len(fields) > 1:
            for phone in fields[1:]:
                if phone not in contact_phones:
                    return f"There is no contact {name} with the phone {phone}"

        contact_phones = "; ".join(contact_phones)

        return f"{name}: {contact_phones}"


class Record:

    def __init__(self, name):
        self.name = name
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def ext_fields(self, fields):
        self.fields.extend(fields)

    def del_field(self, field):
        self.fields.remove(field)

    def change_fields(self, old_field, new_field):
        
        for field in self.fields:
            if field.value == old_field:
                old_field = field

        if isinstance(old_field, str):
            return f"There is no such phone {old_field} in the contact with name {self.name.value}"

        index = self.fields.index(old_field)
        self.fields.pop(index)
        self.fields.insert(index, new_field)

        return "Fields changed successfully"


class Field:

    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass