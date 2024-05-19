# Ковариантность и контравариантность
В Java, можно создавать ковариантные и контравариантные дженерики, явно указав отношение между обобщенным типом и некоторым другим типом при помощи _<? extends T>_ или _<? super T>_.

**Определения типов:**
```java
import java.util.ArrayList;
import java.util.List;

class Animal {
    public void makeSound() {
        System.out.println("Some generic animal sound");
    }
}

class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof");
    }
}

class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Meow");
    }
}
```
\
**Ковариантная функция, принимающая параметризованную коллекцию.** В данном случае, коллекции типов-наследников будут являться потомками коллекции _Animal_.
```java
public class Main  {
    public static void makeAllAnimalsSound(List<? extends Animal> animals) {
        for (Animal animal : animals) {
            animal.makeSound();
        }
    }

    public static void main(String[] args) {
        List<Animal> animals = new ArrayList<>();
        List<Dog> dogs = new ArrayList<>();
        List<Cat> cats = new ArrayList<>();

        dogs.add(new Dog());
        cats.add(new Cat());
        animals.add(new Dog());
        animals.add(new Cat());

        makeAllAnimalsSound(dogs);
        makeAllAnimalsSound(cats);
        makeAllAnimalsSound(animals);
        
        // Output: Woof Meow Woof Meow
    }
}
```
\
**Контравариантная функция, принимающая параметризованную коллекцию.** В данном случае, коллекция _Animal_ будут являться потомком коллекции _Dog_. Коллекция _Cat_ будет в этом контексте инвариантной, так как множества кошек и собак не пересекаются.
```java
public class Main  {
    public static void addDog(List<? super Dog> animals) {
        animals.add(new Dog());
    }

    public static void main(String[] args) {
        List<Animal> animals = new ArrayList<>();
        List<Dog> dogs = new ArrayList<>();
        List<Cat> cats = new ArrayList<>();

        addDog(animals);
        addDog(dogs);
        // addDog(cats); // Error
    }
}
```