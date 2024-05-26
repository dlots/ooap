# Добавим ещё больше строгости
## C++
### Ковариантные вызовы (шаблоны)
```cpp
#include <iostream>
#include <vector>

template <typename T>
class Container {
public:
    void add(const T& item) {
        items.push_back(item);
    }

    void display() const {
        for (const auto& item : items) {
            item.display();
        }
    }

private:
    std::vector<T> items;
};

class Animal {
public:
    void display() const {
        std::cout << "Animal" << std::endl;
    }
};

class Dog : public Animal {
public:
    void display() const {
        std::cout << "Dog" << std::endl;
    }
};

int main() {
    Container<Animal> animalContainer;
    Animal animal;
    Dog dog;

    animalContainer.add(animal);
    animalContainer.add(dog); // Dog является производным от Animal

    animalContainer.display(); // Выводит "Animal" и "Animal", так как базовый тип Animal

    return 0;
}
```

### Полиморфные вызовы (виртуальные методы)
```cpp
#include <iostream>

class Animal {
public:
    virtual void makeSound() const {
        std::cout << "Some sound" << std::endl;
    }

    virtual ~Animal() = default; // Виртуальный деструктор
};

class Dog : public Animal {
public:
    void makeSound() const override {
        std::cout << "Bark" << std::endl;
    }
};

class Cat : public Animal {
public:
    void makeSound() const override {
        std::cout << "Meow" << std::endl;
    }
};

void playSound(const Animal& animal) {
    animal.makeSound();
}

int main() {
    Dog myDog;
    Cat myCat;

    playSound(myDog); // Выводит "Bark"
    playSound(myCat); // Выводит "Meow"

    return 0;
}
```