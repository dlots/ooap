import copy
import json
from abc import ABC, abstractmethod

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


class Animal(Any):
    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        print('Woof!')


class Cat(Animal):
    def speak(self):
        print('Meow!')


class Human(Animal):
    def speak(self):
        print('Hi!')


class Machine(Any):
    @abstractmethod
    def press_button(self):
        pass


class Bomb(Machine):
    def press_button(self):
        print('BOOM')


class Void(Dog, Cat, Human, Bomb):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Void, cls).__new__(cls)
        return cls._instance


def make_animal_speak(animal: Animal):
    if not isinstance(animal, Any):
        print('Please use our type system! What is', type(animal), '?')
        return
    if not isinstance(animal, Animal):
        print(animal.print(), "is not an animal!")
        return
    if animal == Void():
        print('Animal does not exist!')
        return
    animal.speak()


if __name__ == '__main__':
    me = Human()
    my_pet = Cat()
    friends_pet = Dog()
    neighbors_pet = Void()
    animal_shaped_bomb = Bomb()
    local_animals = [me, my_pet, friends_pet, neighbors_pet, animal_shaped_bomb, None]
    for animal in local_animals:
        make_animal_speak(animal)
    # OUTPUT:
    #   Hi!
    #   Meow!
    #   Woof!
    #   Animal does not exist!
    #   Bomb{} is not an animal!
    #   Please use our type system! What is <class 'NoneType'> ?