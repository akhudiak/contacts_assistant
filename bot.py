EXIT = ["good bye", "close", "exit"]
contacts = {}


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

    name = args[0]
    
    if name in contacts:
        raise ValueError
    
    phone_num = args[1]
    contacts[name] = phone_num

    return "Сontact added successfully"


@input_error
def change(args):

    name = args[0]

    if name not in contacts:
        raise ValueError
    
    phone_num = args[1]
    contacts[name] = phone_num

    return "Сontact changed successfully"


@input_error
def phone(args):

    name = args[0]

    if name not in contacts:
        raise ValueError

    return f"{name}: {contacts[name]}"


def show_all(args):
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def no_command(args):
    return "Wrong command! Try again."


COMMANDS = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all
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