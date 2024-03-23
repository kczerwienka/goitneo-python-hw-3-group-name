def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter correct user name."
        except IndexError:
            return "Wrong index."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts.keys():
        return "Contact already exists."
    else:
        contacts[name] = phone
        return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    check_if_exist = contacts[name]
    contacts.update({name: phone})
    return "Contact changed."

@input_error
def phone_contact(args, contacts):
    name = args
    name = "".join(name)
    return contacts[name]
    
def all_contacts(contacts):
    str=""
    for k, v in contacts.items():
        str += ('{:<10} {:<10}\n'.format(k, v))
    str=str.rstrip("\n")
    return str

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(phone_contact(args, contacts))
        elif command == "all":
            print(all_contacts(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()