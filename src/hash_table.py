from abc import ABC, abstractmethod
from enum import Enum


class SeekStatus(Enum):
    Nil = 0
    Ok = 1
    IsNone = 2


class PutStatus(Enum):
    Nil = 0
    Ok = 1
    IsNone = 2,
    Fail = 3,
    Exists = 4  # May be used in inherited classes


class RemoveStatus(Enum):
    Nil = 0
    Ok = 1,
    IsNone = 2,
    NotFound = 3


# Definition of the abstract data type
# Supports storing several equal values, all copies occupy one capacity slot
class AbstractHashTable(ABC):
    @abstractmethod
    # Post-condition: a new hash table that can store 'capacity' unique values is created
    def __init__(self, capacity):
        pass

    # Return the number of unique elements
    @abstractmethod
    def size(self):
        pass

    # Pre-condition: the value to search is not None
    @abstractmethod
    def seek(self, value):
        pass

    # Pre-condition:  table has a slot for value, the value is not None
    # Post-condition: a new value is inserted to a table, if collision is resolved successfully
    # If value existed prior to the insertion, capacity is not consumed
    @abstractmethod
    def put(self, value):
        pass

    # Pre-condition: value exists in the table, the value is not None
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

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.data = [None] * capacity
        self.capacity = capacity
        self.__size = 0
        self.__seek_status = SeekStatus.Nil
        self._put_status = PutStatus.Nil
        self.__remove_status = RemoveStatus.Nil

    def size(self):
        return self.__size

    def __hash_fun(self, value):
        return sum([ord(ch) for ch in value]) % self.capacity

    def __get_index(self, value):
        return self.__hash_fun(value) % self.capacity

    def seek(self, value):
        if value is None:
            self.__seek_status = SeekStatus.IsNone
            return False
        self.__seek_status = SeekStatus.Ok
        if self.__size == 0:
            return False
        index = self.__get_index(value)
        bucket = self.data[index]
        return bucket is not None and any(entry[0] == value for entry in bucket)

    def put(self, value):
        if value is None:
            self._put_status = PutStatus.IsNone
            return
        self._put_status = PutStatus.Ok
        self.__size += 1
        index = self.__get_index(value)
        bucket = self.data[index]
        if bucket is None:
            self.data[index] = [(value, 1)]
            return
        for i, (stored_value, count) in enumerate(bucket):
            if stored_value == value:
                bucket[i] = (value, count + 1)
                return
        bucket.append((value, 1))

    def remove(self, value):
        if value is None:
            self.__remove_status = RemoveStatus.IsNone
            return
        if self.__size == 0:
            self.__remove_status = RemoveStatus.NotFound
            return
        index = self.__get_index(value)
        bucket = self.data[index]
        if bucket is None:
            self.__remove_status = RemoveStatus.NotFound
            return
        for i, (stored_value, count) in enumerate(bucket):
            if stored_value != value:
                continue
            self.__size -= 1
            self.__remove_status = RemoveStatus.Ok
            if count > 1:
                bucket[i] = (value, count - 1)
                return
            bucket.pop(i)
            if len(bucket) == 0:
                self.data[index] = None
            return
        self.__remove_status = RemoveStatus.NotFound

    def get_seek_status(self):
        return self.__seek_status

    def get_put_status(self):
        return self._put_status

    def get_remove_status(self):
        return self.__remove_status
