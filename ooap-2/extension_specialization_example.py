# Example of extension


# Base class
class Animal:
    def __init__(self, species, age):
        self.species = species
        self.age = age

    def eat(self):
        print(f"The {self.species} is eating.")


# Child class extending Animal
class Dog(Animal):
    def __init__(self, species, age, breed):
        super().__init__(species, age)
        self.breed = breed

    def bark(self):
        print(f"The {self.breed} is barking.")


# Example usage
my_dog = Dog("Canine", 3, "Labrador")
my_dog.eat()  # Inherited from Animal
my_dog.bark()  # Unique to Dog


####################################################


#  Example of specialization


# Base class
class Shape:
    def area(self):
        return 0


# Child class specializing Shape
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius


# Example usage
circle = Circle(5)
print("Area of the circle:", circle.area())
