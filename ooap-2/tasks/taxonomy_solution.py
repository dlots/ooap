# Плохой дизайн с использованием флагов:
class Viewer:
    def __init__(self, mature_contend_allowed=true, shocking_content_allowed=true):
        self.__mature_content_allowed = mature_contend_allowed
        self.__shocking_content_allowed = shocking_content_allowed

    def __filter_mature(self, content):
        pass

    def __filter_shocking(self, content):
        pass

    def __get_content(self):
        pass

    def get_subscribed_content(self):
        result = self.__get_content()
        if not self.__mature_content_allowed:
            self.__filter_mature(result)
        if not self.__shocking_content_allowed:
            self.__filter_shocking(result)
        return result

# Произошел сбой, флажок в аккаунте ребенка оказался true, ребенок увидел плохой контент = LAWSUIT


# Полиморфный дизайн
# Не очень хороший пример получился, тут больше подходит паттерн "Декоратор" или что-то подобное.
# Но для демонстрации отвязки от "флагов" и использования иерархии для изменения поведения, подходит.
class Viewer:
    def __get_content(self):
        pass

    def get_subscribed_content(self):
        result = self.__get_content()
        return result


class FilteredViewer(Viewer):
    @abstractMethod
    def __filter(self, content):
        pass

    def get_subscribed_content(self):
        return self.__filter(super().get_subscribed_content())


class MatureForbiddenViewer(FilteredViewer):
    def __filter(self, content):
        pass


class ShockingForbiddenViewer(FilteredViewer):
    def __filter(self, content):
        pass


class ChildViewer(MatureForbiddenViewer, ShockingForbiddenViewer):
    def get_subscribed_content(self):
        result = super().get_subscribed_content()
        result = MatureForbiddenViewer.__filter(result)
        result = ShockingForbiddenViewer.__filter(result)
        return result
