from data_structure import AddressBook, Record, Name, Phone, Birthday
from exceptions import IncorrectPhone, IncorrectBirthday, FlagError, SearchError, SearchArgumentCountError


EXIT = ["good bye", "close", "exit"]
FILE = "contacts.bin"

try:
    contacts = AddressBook.load_from_file(FILE)
except FileNotFoundError:
    contacts = AddressBook()


def input_error(func):

    def wrapper(args):
        try:
            return func(args)
        except IndexError:
            return "Give me all needed data"
        except ValueError:
            return "Error in the contact name!"
        except IncorrectPhone:
            return "There is incorrect symbol in phone number"
        except IncorrectBirthday:
            return "Incorrect format of birthday. Must be dd.mm.yyyy"
        except FlagError:
            return "Error in flag format. Must be 'flag'='value'"
        except SearchError as error:
            return error
        except SearchArgumentCountError:
            return "Must be only 1 argument (search 'info')"

    return wrapper


def flag_split_data(arg):
    try:
        flag, data = arg.split("=")
        return flag, data
    except ValueError:
        raise FlagError


def hello(args):
    return "How can I help you?"


@input_error
def add_contact(args):

    name = Name(args[0])
    
    if name.value in contacts:
        raise ValueError
    
    record = Record(name)
    
    if len(args) > 1:

        for arg in args[1:]:
            
            flag, data = flag_split_data(arg)
            
            if flag == "p":
                phone = Phone(data)
                record.add_phone(phone)
            elif flag == "b":
                record.birthday = Birthday(data)

    contacts.add_record(record)

    return "Contact added successfully"


@input_error
def delete_contact(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError

    contacts.del_record(name)

    return "Contact delete successfully"


@input_error
def search_info(args):

    if len(args) > 1:
        raise SearchArgumentCountError

    user_input = args[0]
    result = []

    for contact in contacts.values():

        if user_input in str(contact):
            result.append(str(contact))

    if not result:
        raise SearchError(user_input)
    
    return "\n".join(result)


def show_all(args):

    filler = "-"
    filler_length = 100

    print("Start\n" + filler * filler_length)

    try:
        contacts_per_page = int(args[0])

    except ValueError:

        names = contacts

        for name in names:

            phones = "; ".join([phone.value for phone in contacts[name].phones])
            print(f"{name}: {phones}")

        print(filler * filler_length)

    else:

        names_iterator = contacts.iterator(contacts_per_page)

        for names in names_iterator:

            for name in names:

                phones = "; ".join([phone.value for phone in contacts[name].phones])
                print(f"{name}: {phones}")

            print(filler * filler_length, input())

    return "End"


@input_error
def add_phones(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError
    else:
        record = contacts[name]
    
    if len(args) > 1:
        for arg in args[1:]:
            phone = Phone(arg)
            record.add_phone(phone)
    # якщо вказане тільки ім'я, то телефони не додаються і виводиться, що телефони були додані
    return "Phones added successfully"


@input_error
def delete_phones(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError
    else:
        record = contacts[name]
    
    if len(args) > 1:

        for arg in args[1:]:
            for phone in record.phones:
                if arg == phone.value:
                    record.del_phone(phone)

    else:
        record.phones = []

    return "Phones deleted successfully"


@input_error
def change_phones(args):

    name = args[0]

    if name not in contacts:
        raise ValueError
    
    if len(args) < 3:
        raise IndexError
    
    old_phone = args[1]
    new_phone = Phone(args[2])

    return contacts[name].change_phones(old_phone, new_phone)


@input_error
def days_to_birthday(args):
    
    name = args[0]

    if name not in contacts:
        raise ValueError
    
    return contacts[name].days_to_birthday()


def wrong_command(args):
    return "Wrong command! Try again."


COMMANDS = {
    "hello": hello,
    "add": add_contact,
    "delete": delete_contact,
    "search": search_info,
    "show all": show_all,
    "phones add": add_phones,
    "phones delete": delete_phones,
    "phones change": change_phones,
    "days to birthday": days_to_birthday
}


def handler(text):

    for command in COMMANDS:
        if text.lower().startswith(command):
            return COMMANDS[command], text[len(command):].strip().split(" ")
    
    return wrong_command, None
