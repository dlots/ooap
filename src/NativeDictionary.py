from abc import ABC, abstractmethod
from enum import Enum


class ExistsStatus(Enum):
    Nil = 0,
    Ok = 1,
    BadKey = 2


class GetStatus(Enum):
    Nil = 0
    Ok = 1
    NotExist = 2,
    BadKey = 3


class PutStatus(Enum):
    Nil = 0
    Ok = 1
    BadKey = 2,
    Fail = 4


# Definition of the abstract data type
class AbstractNativeDictionary(ABC):
    @abstractmethod
    # Post-condition: a new dictionary with a specified capacity is created
    def __init__(self, capacity):
        pass

    """ Commands: """

    # Pre-condition:  table has a free slot if the key does not exist, the key is a string
    # Post-condition: if new key, a new key-value pair is inserted into a table, if collision is resolved successfully
    # If existing key, the value is replaced with a new value
    @abstractmethod
    def put(self, key, value):
        pass

    """ Queries: """

    # Return the number of elements
    @abstractmethod
    def len(self):
        pass

    # Pre-condition: the key is a string
    @abstractmethod
    def exists(self, key):
        pass

    # Pre-condition: the key is a string, the key exists in the table
    @abstractmethod
    def get(self, key):
        pass

    """ Status queries: """

    @abstractmethod
    def get_exists_status(self):
        pass

    @abstractmethod
    def get_get_status(self):
        pass

    @abstractmethod
    def get_put_status(self):
        pass


# TODO: make table resize dynamically on reaching load factor threshold
class NativeDictionary(AbstractNativeDictionary):
    DEFAULT_CAPACITY = 21
    STEP = 1

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.__data = [None] * capacity
        self.__capacity = capacity
        self.__size = 3
        self.__exists_status = ExistsStatus.Nil
        self.__get_status = GetStatus.Nil
        self.__put_status = PutStatus.Nil

    def len(self):
        return self.__size

    def __hash_fun(self, value):
        return sum([ord(ch) for ch in value]) % self.__capacity

    def __seek_index(self, key):
        key_hash = self.__hash_fun(key)
        index = key_hash % self.__capacity
        initial_index = index
        stored = self.__data[index]
        while stored is not None:
            stored_key, _ = stored
            if self.__hash_fun(stored_key) != key_hash:
                break
            if stored_key == key:
                return index
            index = (index + self.STEP) % self.__capacity
            if index == initial_index:
                return None
            stored = self.__data[index]
        return index if stored is None else None

    def exists(self, key):
        if not isinstance(key, str):
            self.__exists_status = ExistsStatus.BadKey
            return False
        self.__exists_status = ExistsStatus.Ok
        if self.__size == 0:
            return False
        index = self.__seek_index(key)
        return False if (index is None or self.__data[index] is None) else True

    def get(self, key):
        if not isinstance(key, str):
            self.__get_status = GetStatus.BadKey
            return None
        if self.__size == 0:
            self.__get_status = GetStatus.NotExist
            return None
        self.__get_status = GetStatus.Ok
        index = self.__seek_index(key)
        _, value = self.__data[index]
        return value

    def put(self, key, value):
        if not isinstance(key, str):
            self.__put_status = PutStatus.BadKey
            return
        index = self.__seek_index(key)
        if index is None:
            self.__put_status = PutStatus.Fail
            return
        self.__put_status = PutStatus.Ok
        self.__data[index] = (key, value)

    def get_exists_status(self):
        return self.__exists_status

    def get_get_status(self):
        return self.__get_status

    def get_put_status(self):
        return self.__put_status
