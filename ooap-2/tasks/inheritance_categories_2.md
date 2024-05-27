# Категории наследования 2
4. **Наследования вариаций**
   - **Наследование с функциональной вариацией**:
     ```cpp
     class Connection {
     public:
        virtual void sendData(Data& data) {
            // send data
        }
     };
     
     class SecureConnection : public Connection {
     public:
        virtual void sendData(Data& data) override {
            encryptData(data);
            Connection::sendData(data);
        }
     
     private:
        void encryptData(Data& data) {
            // encrypt data
        }
     };
     ```
   - **Наследование с вариацией типа**:
     ```cpp
     class Call {
     public:
         void setInputDevice(const AudioInputDevice& device) {
             audioInputDevice = device;
         }
     private:
        AudioInputDevice audioInputDevice;
     };
     
     class VideoCall : public Call {
     public:
         void setInputDevice(const VideoInputDevice& device) {
             videoInputDevice = device;
         }
     private:
        VideoInputDevice audioInputDevice;
     // также наследует родительские методы и поля
     };
     ```
5. **Наследование с конкретизацией**:
```cpp
class HashHandler {
public:
    virtual std::string hash(const Data& data) = 0;
}

class SHA512Handler : public HashHandler {
public:
    std::string hash(const Data& data) override;
}

class MD5Handler : public HashHandler {
public:
    std::string hash(const Data& data) override;
}
```
6. **Структурное наследование**:
```cpp
class Stateful {
public:
    virtual void saveState() = 0;
    virtual void loadState() = 0;
};

class Widget {
public:
    virtual void display() const;
    void setData(const std::string& newData);
};

// Класс StatefulWidget, наследующий Widget и Stateful
class StatefulWidget : public Widget, public Stateful {
public:
    void saveState() override;
    void loadState() override;
};
```