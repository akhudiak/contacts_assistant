from data_structure import AddressBook, Record, Name, Phone


EXIT = ["good bye", "close", "exit"]
contacts = AddressBook()


def input_error(func):

    def wrapper(args):
        try:
            return func(args)
        except IndexError:
            return "Give me all needed data."
        except ValueError:
            return "Error in the contact name!"

    return wrapper


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
            phone_num = Phone(arg)
            record.add_field(phone_num)

    contacts.add_record(record)

    return "Сontact added successfully"


@input_error
def delete(args):

    name = args[0]
    
    if name not in [key for key in contacts.keys()]:
        raise ValueError

    contacts.del_record(name)

    return "Сontact delete successfully"


@input_error
def change(args):

    name = args[0]

    if name not in contacts:
        raise ValueError
    
    fields = []

    if len(args) > 1:
        fields = list(map(lambda arg: Phone(arg), args[1:]))

    contacts.change_record(name, fields)

    return "Сontact changed successfully"


def search(args):
    return contacts.search_record(args)


def show_all(args):

    all = []

    for name, record in contacts.items():

        fields = "; ".join([field.value for field in record.fields])
        all.append(f"{name}: {fields}")

    return "\n".join(all)


@input_error
def add_fields(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError
    else:
        record = contacts[name]
    
    if len(args) > 1:
        for arg in args[1:]:
            phone_num = Phone(arg)
            record.add_field(phone_num)

    return "Fields added successfully"


@input_error
def delete_fields(args):

    name = args[0]
    
    if name not in contacts:
        raise ValueError
    else:
        record = contacts[name]
    
    if len(args) > 1:

        for arg in args[1:]:
            for phone in record.fields:
                if arg == phone.value:
                    record.del_field(phone)

    else:
        record.fields = []

    return "Fields deleted successfully"


@input_error
def change_fields(args):

    name = args[0]

    if name not in contacts:
        raise ValueError
    
    if len(args) < 3:
        raise IndexError
    
    old_field = args[1]
    new_field = Phone(args[2])

    return contacts[name].change_fields(old_field, new_field)


def no_command(args):
    return "Wrong command! Try again."


COMMANDS = {
    "hello": hello,
    "add": add,
    "delete": delete,
    "change": change,
    "search": search,
    "show all": show_all,
    "fields add": add_fields,
    "fields delete": delete_fields,
    "fields change": change_fields
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