# Принцип Открыт/Закрыт применительно к иерархии классов
В С++ нельзя переопределить не виртуальную функцию, поэтому методы базового класса General не нужно дополнительно защищать.
Вместе с этим, если некоторый метод должен быть виртуальным, но на определенной ступени иерархии его необходимо защитить от изменения, можно использовать ключевое слово final.
```cpp
class Npc {
public:
// commands:
    virtual void onPlayerNoticed(const PlayerCharacter& player) = 0;

// queries:
...
// status queries:
...
}

class Monster : public Npc {
public:
    // Атакует
    virtual void onPlayerNoticed(const PlayerCharacter& player) override;
...
}

class Villager : public Npc {
public:
    // Приветствует (Проигрывает звук и анимацию, идентификаторы ресурсов приветствия будут меняться в потомках,
    // но алгоритм останется неизменным, поэтому запрещаем переопределять метод потомкам.
    virtual void onPlayerNoticed(const PlayerCharacter& player) final;
    
private:
    std::vector<Resource> greetingResources;
...
}

class Trader : public Villager {
public:
    void onTradeRequest(const PlayerCharacter& player);
// Также унаследовал onPlayerNoticed, не может переопределить его.
...
}
```
Также можно запретить наследоваться от класса вообще, например, когда не имеет смысла иметь потомков.
```cpp
class UiScreen {
public:
    virtual void open() = 0;
    ...
}

// Этот класс может иметь наследников (например, GlobalMap, CityMap, DungeonMap, etc...)
class Map : public UiScreen {
public:
    virtual void open() override;
    ...
}

// От этого класса нельза наследоваться
class Inventory final : public UiScreen {
public:
    virtual void open() override;
...
}
```