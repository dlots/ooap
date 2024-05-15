# Динамическое связывание

## Пример на C++
В C++ есть и статическое связывание (перегрузка методов), и динамическое (виртуальное методы). Пример динамического связывания:
```cpp
// Базовый класс Animal
class Animal {
public:
    virtual void makeSound() {
        std::cout << "Some generic animal sound\n";
    }
};

// Специализация Dog
class Dog : public Animal {
public:
    void makeSound() override {
        std::cout << "Woof! Woof!\n";
    }
};

// Специализация Cat
class Cat : public Animal {
public:
    void makeSound() override {
        std::cout << "Meow! Meow!\n";
    }
};

int main() {
    // Указатель на базовый класс Animal
    std::shared_ptr<Animal> animal;

    // Указатель animal указывает на объект типа Dog
    animal = std::make_shared<Dog>();
    // Вызов метода makeSound() будет динамически связан с реализацией в классе Dog
    animal->makeSound(); // Вывод: Woof! Woof!

    // Указатель animal указывает на объект типа Cat
    animal = std::make_shared<Cat>();
    // Вызов метода makeSound() будет динамически связан с реализацией в классе Cat
    animal->makeSound(); // Вывод: Meow! Meow!

    return 0;
}
```

## Пример на Python
Так как Python - интерпретируемый язык, в нем есть только динамическое связывание, более того, используется так называемая "утиная типизация" - если у объекта есть вызываемый метод, он может быть вызван, независимо от типа объекта (вызывающий может и не знать тип).
```python
# Базовый класс Animal
class Animal:
    def make_sound(self):
        # Виртуальный метод, который будет переопределен в производных классах
        print("Some generic animal sound")

# Специализация Dog
class Dog(Animal):
    def make_sound(self):
        # Переопределение метода make_sound для класса Dog
        print("Woof! Woof!")

# Специализация Cat
class Cat(Animal):
    def make_sound(self):
        # Переопределение метода make_sound для класса Cat
        print("Meow! Meow!")

# Функция, принимающая объект и вызывающая метод make_sound
def make_animal_sound(animal):
    animal.make_sound()  # Динамическое связывание вызывает правильный метод

# Создание объектов различных классов
dog = Dog()
cat = Cat()

# Вызов функции make_animal_sound с разными объектами
make_animal_sound(dog)  # Вывод: Woof! Woof!
make_animal_sound(cat)  # Вывод: Meow! Meow!
```