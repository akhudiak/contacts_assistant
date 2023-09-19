from bot import contacts, EXIT, FILE, handler


def main():
    
    while True:

        user_input = input(">>> ")

        if user_input.lower() in EXIT:
            contacts.save_to_file(FILE)
            print("Good bye!")
            break

        command, args = handler(user_input)
        
        print(command(args))


if __name__ == "__main__":
    main()
