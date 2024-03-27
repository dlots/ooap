from abc import ABC, abstractmethod
from enum import Enum


class SeekStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2,
    IsNone = 3


class PutStatus(Enum):
    Nil = 0
    Ok = 1
    IsNone = 2,
    Fail = 4


class RemoveStatus(Enum):
    Nil = 0
    Ok = 1,
    IsNone = 2,
    Empty = 3,
    NotFound = 4


# Definition of the abstract data type
# Supports storing several equal values, all copies occupy one capacity slot
class AbstractHashTable(ABC):
    @abstractmethod
    # Post-condition: a new hash table that can store 'capacity' unique values is created
    def __init__(self, capacity):
        pass

    # Return the number of unique elements
    @abstractmethod
    def len(self):
        pass

    # Pre-condition: the table is not empty, the value to search is not None
    @abstractmethod
    def seek(self, value):
        pass

    # Pre-condition:  table has a slot for value, the value is not None
    # Post-condition: a new value is inserted to a table, if collision is resolved successfully
    # If value existed prior to the insertion, capacity is not consumed
    @abstractmethod
    def put(self, value):
        pass

    # Pre-condition: the table is not empty, the value is not None
    # Post-condition: the value is removed from the table if it was unique
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
    STEP = 3

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
        stored = self.__data[index]
        if stored is None:
            self.__size += 1
            self.__data[index] = (value, 1)
            return
        self.__data[index] = (stored[self.VALUE_INDEX], stored[self.COUNT_INDEX] + 1)

    def remove(self, value):
        if self.__size == 0:
            self.__remove_status = RemoveStatus.Empty
            return
        if value is None:
            self.__remove_status = RemoveStatus.IsNone
            return
        index = self.__seek_index(value)
        if index is None or self.__data[index] is None:
            self.__remove_status = RemoveStatus.NotFound
            return
        self.__remove_status = RemoveStatus.Ok
        stored = self.__data[index]
        if stored[self.COUNT_INDEX] == 1:
            self.__size -= 1
            self.__data[index] = None
            return
        self.__data[index] = (stored[self.VALUE_INDEX], stored[self.COUNT_INDEX] - 1)

    def get_seek_status(self):
        return self.__seek_status

    def get_put_status(self):
        return self.__put_status

    def get_remove_status(self):
        return self.__remove_status
