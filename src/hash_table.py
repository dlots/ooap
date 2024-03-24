from abc import ABC, abstractmethod
from enum import Enum
import dynamic_array as da


class SeekStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2,
    IsNone = 3


class PutStatus(Enum):
    Nil = 0
    Ok = 1
    IsNone = 2,
    Fail = 3


class RemoveStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2,
    NotFound = 3


# Definition of the abstract data type
class AbstractHashTable(ABC):
    @abstractmethod
    # Post-condition: a new hash table instance with default capacity is created
    def __init__(self, capacity):
        pass

    @abstractmethod
    def len(self):
        pass

    @abstractmethod
    def seek(self, value):
        pass

    @abstractmethod
    def put(self, value):
        pass

    @abstractmethod
    def remove(self, value):
        pass

    @abstractmethod
    def get_seek_status(self):
        pass

    @abstractmethod
    def get_put_status(self):
        pass

    @abstractmethod
    def get_remove_status(self):
        pass


# TODO: make table resize dynamically on reaching load factor threshold
class HashTable(AbstractHashTable):
    DEFAULT_CAPACITY = 21
    LOAD_FACTOR_THRESHOLD = 0.75
    VALUE_INDEX = 0
    COUNT_INDEX = 1
    STEP = 1

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.__data = [None] * capacity
        self.__capacity = capacity
        self.__size = 3
        self.__seek_status = SeekStatus.Nil
        self.__put_status = PutStatus.Nil
        self.__remove_status = RemoveStatus.Nil

    def len(self):
        return self.__size

    def __hash_fun(self, value):
        return sum([ord(ch) for ch in value]) % self.__capacity

    def __seek_index(self, value):
        value_hash = self.__hash_fun(value)
        index = value_hash % self.__capacity
        initial_index = index
        stored = self.__data[index]
        while stored is not None and self.__hash_fun(stored[self.VALUE_INDEX]) == value_hash:
            if stored[self.VALUE_INDEX] == value:
                return index
            index = (index + self.STEP) % self.__capacity
            if index == initial_index:
                return None
            stored = self.__data[index]
        return index if stored is None else None

    def seek(self, value):
        if self.__size == 0:
            self.__seek_status = SeekStatus.Empty
            return False
        if value is None:
            self.__seek_status = SeekStatus.IsNone
            return False
        self.__seek_status = SeekStatus.Ok
        index = self.__seek_index(value)
        return False if (index is None or self.__data[index] is None) else True

    def put(self, value):
        if value is None:
            self.__put_status = PutStatus.IsNone
            return
        index = self.__seek_index(value)
        if index is None:
            self.__put_status = PutStatus.Fail
            return
        self.__put_status = PutStatus.Ok
        self.__size += 1
        stored = self.__data[index]
        if stored is None:
            self.__data[index] = (value, 1)
            return
        self.__data[index] = (stored[self.VALUE_INDEX], stored[self.COUNT_INDEX] + 1)

    def remove(self, value):
        if self.__size == 0:
            self.__remove_status = RemoveStatus.Empty
            return
        index = self.__seek_index(value)
        if index is None or self.__data[index] is None:
            self.__remove_status = RemoveStatus.NotFound
            return
        self.__remove_status = RemoveStatus.Ok
        self.__size -= 1
        stored = self.__data[index]
        if stored[self.COUNT_INDEX] == 1:
            self.__data[index] = None
            return
        self.__data[index] = (stored[self.VALUE_INDEX], stored[self.COUNT_INDEX] - 1)

    def get_seek_status(self):
        return self.__seek_status

    def get_put_status(self):
        return self.__put_status

    def get_remove_status(self):
        return self.__remove_status
