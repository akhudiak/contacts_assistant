from data_structure import AddressBook, Record, Name, Phone, Birthday
from exceptions import IncorrectPhone, IncorrectBirthday, FlagError

EXIT = ["good bye", "close", "exit"]
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

    return wrapper


def flag_split_data(args):
    try:
        flag, data = args.split("=")
        return flag, data
    except ValueError:
        raise FlagError


def hello(args):
    return "How can I help you?"


@input_error
def add(args):

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

    return "Сontact added successfully"


@input_error
def delete(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError

    contacts.del_record(name)

    return "Сontact delete successfully"


def search(args):

    name = args[0]

    if name not in contacts:
        return f"There is no contact with the name {name}"
    
    phones = [phone.value for phone in contacts[name].phones]

    if len(args) > 1:

        for arg in args[1:]:

            flag, data = flag_split_data(arg)

            if flag == "p":

                if data not in phones:
                    return f"There is no contact {name} with the phone {data}"

    phones = "; ".join(phones)
    
    return f"{name}: {phones}"


def show_all(args):

    filler = "-"
    filler_length = 30

    print("Start\n" + filler * filler_length)

    try:
        n = int(args[0])

    except ValueError:

        all_names = contacts

        for name in all_names:

            phones = "; ".join([phone.value for phone in contacts[name].phones])
            print(f"{name}: {phones}")

        print(filler * filler_length)

    else:

        all_names =  contacts.iterator(n)

        for names in all_names:

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


def no_command(args):
    return "Wrong command! Try again."


COMMANDS = {
    "hello": hello,
    "add": add,
    "delete": delete,
    "search": search,
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
    
    return no_command, None


def main():
    
    while True:

        user_input = input(">>> ")

        if user_input.lower() in EXIT:
            print("Good bye!")
            break

        command, args = handler(user_input)
        
        print(command(args))


if __name__ == "__main__":
    main()