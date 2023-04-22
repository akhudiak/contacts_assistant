EXIT = ["good bye", "close", "exit"]
contacts = {}


def input_error(func):

    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Wrong command! Try again."
        except IndexError:
            return "Give me all needed data."
        except ValueError:
            return "Error in the contact name!"

    return wrapper


def hello(*args):
    return "How can I help you?"


@input_error
def add(*args):

    name = args[0]
    
    if name in contacts:
        raise ValueError
    
    phone_num = args[1]
    contacts[name] = phone_num

    return "Сontact added successfully"


@input_error
def change(*args):

    name = args[0]

    if name not in contacts:
        raise ValueError
    
    phone_num = args[1]
    contacts[name] = phone_num

    return "Сontact changed successfully"


@input_error
def phone(*args):

    name = args[0]

    if name not in contacts:
        raise ValueError

    return f"Name: {name}. Phone number: {contacts[name]}"


def show_all(*args):
    pass


COMMANDS = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all
}


@input_error
def handler(command):
    return COMMANDS[command]


def main():
    
    while True:

        user_input = input(">>> ")

        if user_input in EXIT:
            print("Good bye!")
            break

        user_input = user_input.split(" ")

        get_handler = handler(user_input[0].lower())
        
        try:
            print(get_handler(*user_input[1:]))
        except TypeError:
            print(get_handler)

        print(contacts)


if __name__ == "__main__":
    main()