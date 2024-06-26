# Модульное противоречие
## 1. Существуют ли ситуации, когда связи между модулями должны делаться публичными?
Некоторые модули могут раскрывать часть своей функциональности внешним пользователям (другим модулям), в случае, если
необходимо предоставить интерфейс модуля (набор функций, которыми можно вызвать, чтобы воспользоваться функциональностью
модуля), типам, определенным в этом модуле (результат вызова функции или тип для параметров функций интерфейса).
Публично доступную часть модуля необходимо минимизировать, обеспечить большую независимость модулей.
## 2. Какие метрики вы бы предложили для количественной оценки принципов организации модулей
- Число строк/функций в модуле - слишком больший модуль можно разделить на несколько новых модулей
- Число экспортируемых функций, входящих в интерфейс модуля - то же самое, возможно модуль следует разделить
- Сложность модуля (например, цикломатическая) - модуль с запутанным и трудным для понимания кодом может быть тяжело изменить при изменениях в другом модуле, что ухудшает модульность системы
- Число связей модуля с другими модулями (зависимости модуля, и модули, зависимые от модуля) - серьезные изменения в интерфейсе или типах модуля могут повлечь необходимость изменений в других модулях
- Связность элементов модуля друг с другом - насколько тесно взаимодействуют элементы модуля между собой, есть ли элементы, связанные слабо или несвязанные вообще. Распадание графа модуля на подграфы - это признак того, что модуль выполняет несколько различных функций, и должен быть разделен на несколько модулей.
## 3. Если вы разрабатывали программы, в которых было хотя бы 3-5 классов, как бы вы оценили их модульность по этим метрикам?
- Во многих проектах я встречал очень большие модули и классы, которые хотелось разделить на меньше части.
- Раздутый интерфейс класса - также часто встречающаяся проблема. Многие модули и классы предоставляют десятки функций.
- Тоже часто встречающаяся проблема. На прошлой работе зачастую сборки CI/CD падали из-за достижения лимита сложности, когда добавлись новые ветвления, вместо того чтобы сделать рефакторинг части кода с глубокой вложненностью.
- Видел и хорошие, и плохие примеры. Например, в одном из проектов, для обмена данными между модулями использовался механизм "properties", когда классы, нуждающиеся в данных, могут получать их от поставщиков через единый механизм, без необходимости знать, кто именно предоставляет нужную "property". В то же время, всем модулям был доступен глобальный контекст, из которого можно было напрямую получать доступ к синглтонам и статическим классам; каждое использование этой возможности увеличивает сцепленность модулей в системе.
- "Раздутые" модули склонны распадаться на несколько частей, выполняющих разные функции. Это часто встречается, так как в проектах часто встречаются большие модули/классы.

**Вывод:** На модульность системы влияют как связи между модулями и внутри них, так и качество написания кода. Модульность системы можно оценить конкретными численными метриками.