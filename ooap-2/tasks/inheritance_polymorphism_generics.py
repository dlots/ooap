import copy
import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol

CLASS_KEY = 'class'


# Базовый класс General, реализующий базовую функциональность для всех потомков
# Класс использует рефлексию для выполнения базовых операций
# Это позволяет применить методы ко всем потомкам без переопределения методов
# Все методы объявлены абстрактными, поэтому нельзя создать экземпляр
class General(ABC):
    @abstractmethod
    def copy(self, other):
        if not self.is_same_type(other):
            raise TypeError('Tried to copy another type')
        for key, value in other.__dict__.items():
            self.__dict__[key] = copy.deepcopy(value)

    @abstractmethod
    def clone(self):
        return copy.deepcopy(self)

    @abstractmethod
    def deep_compare(self, other):
        if not self.is_same_type(other):
            return False
        for key, other_value in other.__dict__.items():
            self_value = self.__dict__[key]
            if isinstance(other_value, General) and not other_value.deep_compare(self_value):
                return False
            if self_value != other_value:
                return False
        return True

    @abstractmethod
    def serialize(self):
        to_serialize = copy.deepcopy(self.__dict__)
        to_serialize[CLASS_KEY] = str(self.get_real_type())
        return json.dumps(to_serialize)

    @abstractmethod
    def deserialize(self, data):
        to_deserialize = json.loads(data)
        if str(self.get_real_type()) != to_deserialize[CLASS_KEY]:
            raise TypeError('Wrong deserialized class')
        to_deserialize.pop(CLASS_KEY)
        for key, value in to_deserialize.items():
            self.__dict__[key] = value

    @abstractmethod
    def print(self):
        return self.get_real_type().__name__ + str(self.__dict__)

    @abstractmethod
    def is_instance_of(self, cls):
        return isinstance(self, cls)

    @abstractmethod
    def get_real_type(self):
        return type(self)

    @abstractmethod
    def is_same_type(self, other):
        return self.is_instance_of(type(other))

    @abstractmethod
    def assignment_attempt(self, source):
        if not isinstance(source, self.get_real_type()):
            return Void()
        return source


# Класс Any не определяет новых методов, служит базовым классом для остальной иерархии
class Any(General):
    def copy(self, other):
        super().copy(other)

    def clone(self):
        return super().clone()

    def deep_compare(self, other):
        return super().deep_compare(other)

    def serialize(self):
        return super().serialize()

    def deserialize(self, data):
        super().deserialize(data)

    def print(self):
        return super().print()

    def is_instance_of(self, cls):
        return super().is_instance_of(cls)

    def get_real_type(self):
        return super().get_real_type()

    def is_same_type(self, other):
        return super().is_same_type(other)

    def assignment_attempt(self, source):
        return super().assignment_attempt(source)


class SupportsAddition(Protocol):
    @abstractmethod
    def __add__(self, other: 'SupportsAddition') -> 'SupportsAddition':
        pass


class MyInteger(SupportsAddition, Any):
    def __init__(self, value: int):
        self.__value = value

    def __add__(self, other: 'MyInteger') -> 'MyInteger':
        return MyInteger(self.__value + other.__value)

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self)


T = TypeVar('T', bound=SupportsAddition)


class Vector(Any, SupportsAddition, Generic[T]):
    def __init__(self, data: list[T] = None):
        self.__data = data if data is not None else list[T]()

    def push(self, new_element: T):
        self.__data.append(new_element)

    def __len__(self):
        return len(self.__data)

    def __add__(self, other: 'Vector[T]') -> 'Vector[T]':
        if self == Void() or other == Void() or len(self) != len(other):
            return Void()
        result = Vector()
        result.__data = [a + b for a, b in zip(self.__data, other.__data)]
        return result

    def __str__(self):
        return '[' + ', '.join([repr(element) for element in self.__data]) + ']'

    def __repr__(self):
        return 'Vector{' + ', '.join([repr(element) for element in self.__data]) + '}'


class Void(Any):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Void, cls).__new__(cls)
        return cls._instance

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    a = Vector([MyInteger(1), MyInteger(3)])
    b = Vector([MyInteger(2)])
    c = Vector([a, b])
    d = Vector([a, a])
    print(c)
    print(d)
    print(c + d)
    e = Vector([c, d])
    f = Vector([d, c])
    print(e)
    print(f)
    print(e + e)
    print(e + f)
