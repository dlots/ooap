# Политика скрытия методов при наследовании
## C++
1. метод публичен в родительском классе А и публичен в его потомке B
```cpp
class Base {
public:
    void method();
}

class Derived : public Base {
// void method() наследуется автоматически, видим
}
```
2. метод публичен в родительском классе А и скрыт в его потомке B
```cpp
class Base {
public:
    void method1();
    void method2();
}

// Вариант 1
class Derived : protected Base {
// method1(), method2() наследуются и будут виден только внутри Derived, а также его потомкам, но не снаружи
}

// Вариант 2
class Derived : private Base {
// method1(), method2() наследуются и будут видны только внутри Derived, но не потомкам и не снаружи
}

// Вариант 3
class Derived : public Base {
// method1() наследуется как публичный
private:
    using Base::method2; // метод становится приватным
}

```
3. метод скрыт в родительском классе А и публичен в его потомке B
```cpp
Не поддерживается
```
4. метод скрыт в родительском классе А и скрыт в его потомке B
```cpp
class Base {
private:
    void method();
}

class Derived : public Base {
// void method() наследуется автоматически, скрыт
}
```
