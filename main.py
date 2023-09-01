"""
This script provides a simple user management system that allows users to register,
log in, edit their profile, and change their password.

The script imports the 'users' module, which contains the User class, and the 'getpass' module, 
which is used to securely handle password input.

The script contains three main functions:

1. edit_profile(user_profile: users.User) -> None:
   This function allows users to edit their profile, including their username and phone number,
   change their password, or log out. It takes a User object as input and returns None.

2. password_change(user_profile: users.User) -> None:
   This function allows users to change their password. It takes a User object as input and returns None. 
   The function checks if the old password is correct and if the new password matches the confirmation 
   input before updating the password.

3. main() -> None:
   This function serves as the main entry point for the script. It provides a menu for users to register,
   log in, or exit the program. The function loops until the user chooses to exit.

The script is executed by calling the main() function when the script is run as the main module.
"""
import users
import getpass


def edit_profile(user_profile) -> None:
    """
    This function is used to edit user profile.

    :param user_profile: users.User

    :return: None
    """
    print("1. show profile")
    print("2. edit profile include username and phone number")
    print("3. change password")
    print("4. logout")

    choice = input("Enter your choice: ")
    match choice:
        case "1":
            print(user_profile)
        case "2":
            new_username = input("Enter your new username: ")
            new_phone_number = input("Enter your new phone number: ")
            try:
                user_profile.edit_profile(user_profile.username, new_username, new_phone_number)
            except ValueError as e:
                print(e)
        case "3":
            password_change(user_profile)
        case "4":
            print("You are logged out.")


def password_change(user_profile) -> None:
    """
    This function is used to change user password.

    :param user_profile: users.User

    :return: None
    """
    old_password = getpass.getpass("Enter your old password: ")
    if user_profile.password == user_profile.hash_password(old_password):
        user_entered_password = getpass.getpass("Enter your new password: ")
        if user_entered_password == getpass.getpass("Enter your new password again: "):
            user_profile.set_new_password(user_profile.username, user_entered_password)
            print("Password changed successfully.")
        else:
            print("Passwords do not match.")
    else:
        print("Password is incorrect.")


def main() -> None:
    """
    This function is used to run the program.

    :return: None
    """
    while True:
        print("0. Exit")
        print("1. Register")
        print("2. Login")

        choice = input("Enter your choice: ")

        match choice:
            case "0":
                print("Goodbye!")
                break
            case "1":
                username = input("Enter your username: ")
                password = getpass.getpass("Enter your password: ")
                phone_number = input("Enter your phone number: ")
                try:
                    users.User.register_user(username, password, phone_number)
                except ValueError as e:
                    print(e)
            case "2":
                username = input("Enter your username: ")
                password = getpass.getpass("Enter your password: ")
                try:
                    user = users.User.login(username, password)
                    print(f"Welcome {user.username}")
                    edit_profile(user)

                except ValueError as e:
                    print(e)


if __name__ == '__main__':
    main()
