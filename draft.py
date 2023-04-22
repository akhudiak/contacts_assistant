COMMANDS = {
    "hello": 1,
    "add": 2,
    "change": 3,
    "phone": 4,
    "show all": 5
}

test = "show all df df "
for command in COMMANDS:
    if test.startswith(command):
        print(command)


print("hello dora   dura      ".removeprefix("hello"))