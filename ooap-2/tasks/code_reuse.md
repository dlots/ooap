# Принципы повторного использования модуля

Пять принципов переиспользования кода поддерживаются в C++ при помощи следующих возможностей:
- Параметризация типов другими типами - Шаблоны
- Объединение нескольких функций - Классы и структуры, пространства имен, заголовочные файлы.
- Семейство модулей - Библиотеки, заголовочные файлы (пример - стандартная библиотека stl)
- Динамический полиморфизм - Виртуальные и чистые виртуальные методы, переопределение виртуальных методов
  - (также поддерживается статический полиморфизм при помощи перегрузки методов и функций)
- Интеграция поведения нескольких модулей - Композиция, наследование