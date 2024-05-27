# Категории наследования 3
7. Наследование реализации
```cpp
// Базовый класс Stack
class Stack {
protected:
    std::vector<int> elements;
public:
    void push(int element) {
        elements.push_back(element);
    }

    void pop() {
        if (!elements.empty()) {
            elements.pop_back();
        }
    }

    int top() const {
        if (!elements.empty()) {
            return elements.back();
        }
        throw std::out_of_range("Stack is empty");
    }

    bool isEmpty() const {
        return elements.empty();
    }
};

// Класс MinStack, наследующий Stack и добавляющий новую абстракцию
class MinStack : public Stack {
private:
    std::vector<int> minElements;
public:
    void push(int element) {
        Stack::push(element);
        if (minElements.empty() || element <= minElements.back()) {
            minElements.push_back(element);
        }
    }

    void pop() {
        if (!elements.empty() && elements.back() == minElements.back()) {
            minElements.pop_back();
        }
        Stack::pop();
    }

    int getMin() const {
        if (!minElements.empty()) {
            return minElements.back();
        }
        throw std::out_of_range("MinStack is empty");
    }
};
```
8. Льготное наследование
```cpp
// Базовый класс Exception
class Exception {
protected:
    std::string message;
public:
    Exception(const std::string& msg) : message(msg) {}

    virtual const char* what() const noexcept {
        return message.c_str();
    }
};

// Класс FileNotFoundException, наследующий Exception
class FileNotFoundException : public Exception {
public:
    FileNotFoundException(const std::string& filename)
        : Exception("File not found: " + filename) {}
};

// Класс OutOfMemoryException, наследующий Exception
class OutOfMemoryException : public Exception {
public:
    OutOfMemoryException()
        : Exception("Out of memory") {}
};
```