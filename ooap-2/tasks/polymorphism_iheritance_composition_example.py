# Inheritance
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Composition
class Person:
    def __init__(self, pet):
        self.pet = pet

    def greet_pet(self):
        return f"Hello, {self.pet.speak()}"

# Polymorphism
def make_animal_speak(animal):
    return animal.speak()

# Example usage
dog = Dog()
cat = Cat()
person_with_dog = Person(dog)
person_with_cat = Person(cat)

print(person_with_dog.greet_pet())  # Output: Hello, Woof!
print(person_with_cat.greet_pet())  # Output: Hello, Meow!

print(make_animal_speak(dog))  # Output: Woof!
print(make_animal_speak(cat))  # Output: Meow!
