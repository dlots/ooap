import ctypes
from abc import ABC, abstractmethod
from enum import Enum


class SetCursorStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2
    OutOfBounds = 3


class GetStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2


class ReplaceStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2


class InsertStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2


class RemoveStatus(Enum):
    Nil = 0
    Ok = 1
    Empty = 2


# Definition of abstract data type "DynArray"
class DynArray(ABC):
    @abstractmethod
    # Post-condition: a new dynamic array instance with default capacity is created
    def __init__(self):
        pass

    @abstractmethod
    def len(self):
        pass

    # Post-condition: a new value is added at index [size]
    @abstractmethod
    def append(self, value):
        pass

    # Pre-condition: the array is not empty
    # Post-condition: cursor is set at index [i]
    @abstractmethod
    def set_cursor(self, i):
        pass

    # Pre-condition: the array is not empty
    @abstractmethod
    def get(self):
        pass

    # Pre-condition: the array is not empty
    # Post-condition: the value at cursor is replaced with a new value
    @abstractmethod
    def replace(self, value):
        pass

    # Pre-condition: the array is not empty
    # Post-condition: a new value is inserted at cursor; next values are shifted to the right
    @abstractmethod
    def insert(self, value):
        pass

    # Pre-condition: the array is not Empty
    # Post-condition: the value at cursor is removed from the array; next values are shifted to the left
    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def get_set_cursor_status(self):
        pass

    @abstractmethod
    def get_get_status(self):
        pass

    @abstractmethod
    def get_replace_status(self):
        pass

    @abstractmethod
    def get_insert_status(self):
        pass

    @abstractmethod
    def get_remove_status(self):
        pass


def make_array(capacity):
    return (capacity * ctypes.py_object)()


class DynArrayImpl(DynArray):
    DEFAULT_CAPACITY = 16
    RESIZE_DOWN_THRESHOLD = 0.5
    RESIZE_UP_RATE = 2
    RESIZE_DOWN_RATE = 1.5

    def __init__(self):
        self.__size = 0
        self.__capacity = self.DEFAULT_CAPACITY
        self.__minimal_capacity = self.DEFAULT_CAPACITY
        self.__data = make_array(self.DEFAULT_CAPACITY)
        self.__cursor = 0
        self.__set_cursor_status = SetCursorStatus.Nil
        self.__get_status = GetStatus.Nil
        self.__replace_status = ReplaceStatus.Nil
        self.__insert_status = InsertStatus.Nil
        self.__remove_status = RemoveStatus.Nil

    def __len__(self):
        return self.__size

    """
    DynArray implementation
    """

    def len(self):
        return self.__len__()

    def append(self, value):
        if self.__size == self.__capacity:
            self.__resize(self.RESIZE_UP_RATE * self.__capacity)
        self.__data[self.__size] = value
        self.__size += 1

    def set_cursor(self, i):
        if self.__size == 0:
            self.__set_cursor_status = SetCursorStatus.Empty
            return
        if i < 0 or i >= self.__size:
            self.__set_cursor_status = SetCursorStatus.OutOfBounds
            return
        self.__cursor = i
        self.__set_cursor_status = SetCursorStatus.Ok

    def get(self):
        if self.__size == 0:
            self.__get_status = GetStatus.Empty
            return None
        self.__get_status = GetStatus.Ok
        return self.__data[self.__cursor]

    def replace(self, value):
        if self.__size == 0:
            self.__replace_status = ReplaceStatus.Empty
            return
        self.__replace_status = ReplaceStatus.Ok
        self.__data[self.__cursor] = value

    def insert(self, value):
        if self.__size == 0:
            self.__insert_status = InsertStatus.Empty
            return
        self.__insert_status = InsertStatus.Ok
        if self.__size + 1 > self.__capacity:
            self.__resize(self.RESIZE_UP_RATE * self.__capacity)
        i = self.__cursor
        for x in reversed(range(i, self.__size)):
            self.__data[x + 1] = self.__data[x]
        self.__data[i] = value
        self.__size += 1

    def remove(self):
        if self.__size == 0:
            self.__remove_status = RemoveStatus.Empty
            return
        self.__remove_status = RemoveStatus.Ok
        new_size = self.__size - 1
        new_capacity = max(int(self.__capacity / self.RESIZE_DOWN_RATE), self.__minimal_capacity)
        need_to_shrink = new_size / self.__capacity < self.RESIZE_DOWN_THRESHOLD
        if new_capacity != self.__capacity and need_to_shrink:
            self.__resize(new_capacity)
        self.__size = new_size
        for x in range(self.__cursor, self.__size):
            self.__data[x] = self.__data[x + 1]

    def get_set_cursor_status(self):
        return self.__set_cursor_status

    def get_get_status(self):
        return self.__get_status

    def get_replace_status(self):
        return self.__replace_status

    def get_insert_status(self):
        return self.__insert_status

    def get_remove_status(self):
        return self.__remove_status

    """
    Private methods
    """

    def __resize(self, new_capacity):
        new_data = make_array(new_capacity)
        for i in range(self.__size):
            new_data[i] = self.__data[i]
        self.__data = new_data
        self.__capacity = new_capacity

    """
    Debug and UT
    """

    def get_capacity(self):
        return self.__capacity
