class General(ABC):
    # Закрытый класс с имплементацией общих методов
    pass


class Any(General):
    # Открытый потомок, базовый класс для всех остальных классов
    pass


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