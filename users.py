"""
This module defines a User class that represents a user in a simple authentication system.
The User class provides methods for user registration, login, password management,
and profile editing. It also includes a simple in-memory storage for registered users.

The User class has the following attributes:
- users: A dictionary that stores registered users with their username as the key and the User object as the value.
- id: A unique identifier for each user, generated using the uuid4 function.
- username: The username of the user.
- password: The hashed password of the user.
- phone_number: The phone number of the user.

The User class has the following methods:
- __init__: Initializes a new User object with the given username, password, and optional phone number.
- hash_password: A static method that hashes a given password using the SHA256 algorithm.
- validate_password_length: A static method that validates the length of a given password.
- login: A class method that logs in a user with the given username and password.
- set_new_password: A static method that sets a new password for a user with the given username.
- __repr__: Returns a string representation of the User object.
- register_user: A class method that registers a new user with the given username, password,
    and optional phone number.
- edit_profile: A class method that edits the profile of a user with the given username,
    new_username, and new_phone_number.
- get_user: A class method that gets a user by their username.
- delete_user: A class method that deletes a user by their username.
"""
from uuid import uuid4
import hashlib


class User:
    users = {}

    def __init__(self, username: str, password: str, phone_number: str = None) -> None:
        """
        :param username: Username of the user
        :param password: Password of the user
        :param phone_number: Phone number of the user
        """
        self.id = uuid4()
        self.username = username
        self.__password = self.hash_password(password)
        self.phone_number = phone_number

        self.validate_password_length(password)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the password using SHA256 algorithm

        :param password: Password to be hashed
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_password_length(password: str) -> None:
        """
        Validates the length of the password

        :param password: Password to be validated

        :raises ValueError: If the password is less than 4 characters long
        """
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")

    @classmethod
    def login(cls, username: str, password: str):
        """
        Logs in the user

        :param username: Username of the user
        :param password: Password of the user

        :raises ValueError: If the password is incorrect or the user is not found
        """
        user = cls.get_user(username)
        if user:
            if user.__password == cls.hash_password(password):
                return user
            else:
                raise ValueError("Password is incorrect")
        else:
            raise ValueError("User not found")

    @staticmethod
    def set_new_password(username: str, new_password: str) -> None:
        """
        Sets a new password for the user

        :param username: Username of the user
        :param new_password: New password of the user
        """
        User.validate_password_length(new_password)

        user = User.get_user(username)
        if user:
            user.password = User.hash_password(new_password)
            User.users[username] = user
        else:
            raise ValueError("User not found")

    def __repr__(self) -> str:
        """
        :return: String representation of the user
        """
        return f"User(id={self.id}, username={self.username}, phone_number={self.phone_number})"

    @classmethod
    def register_user(cls, username: str, password: str, phone_number: str = None) -> 'User':
        """
        Registers a new user

        :param username: Username of the user
        :param password: Password of the user
        :param phone_number: Phone number of the user

        :raises ValueError: If the username already exists
        """
        if username in cls.users:
            raise ValueError("Username already exists. Please choose a different one.")

        new_user = cls(username, password, phone_number)
        cls.users[username] = new_user
        return new_user

    @classmethod
    def edit_profile(cls, username: str, new_username: str, new_phone_number: str) -> None:
        """
        Edits the profile of the user

        :param username: Username of the user
        :param new_username: New username of the user
        :param new_phone_number: New phone number of the user

        :raises ValueError: If the user is not found or the new username already exists
        """
        if new_username in cls.users and new_username != username:
            raise ValueError("Username already exists. Please choose a different one.")

        user = cls.get_user(username)
        if user:
            if new_username != username:
                cls.users[new_username] = user
                del cls.users[username]
            user.username = new_username
            user.phone_number = new_phone_number
        else:
            raise ValueError("User not found")

    @classmethod
    def get_user(cls, username: str) -> 'User':
        """
        Gets the user by username

        :param username: Username of the user
        """
        return cls.users.get(username)

    @classmethod
    def delete_user(cls, username: str) -> None:
        """
        Deletes the user by username

        :param username: Username of the user

        :raises ValueError: If the user is not found
        """
        try:
            del cls.users[username]
        except KeyError:
            raise ValueError("User not found")
