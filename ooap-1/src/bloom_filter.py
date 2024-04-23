from abc import ABC, abstractmethod


class AbstractBloomFilter(ABC):
    # Post-condition: Bloom filter with a specified size is created
    @abstractmethod
    def __int__(self, filter_len):
        pass

    # Post-condition: value is added to Bloom filter
    @abstractmethod
    def add(self, str1):
        pass

    @abstractmethod
    def is_value(self, str1):
        pass


def _bit_mask(bit):
    return 1 << bit


class BloomFilter(AbstractBloomFilter):
    def __init__(self, filter_len):
        self.filter_len = filter_len
        self.filter = 0

    def __hash1(self, str1):
        result = 0
        for c in str1:
            result = (result * 17 + ord(c)) % self.filter_len
        return result

    def __hash2(self, str1):
        result = 0
        for c in str1:
            result = (result * 223 + ord(c)) % self.filter_len
        return result

    def __set_bit(self, bit):
        self.filter |= _bit_mask(bit)

    def __get_bit(self, bit):
        return (self.filter & _bit_mask(bit)) != 0

    def add(self, str1):
        self.__set_bit(self.__hash1(str1))
        self.__set_bit(self.__hash2(str1))

    def is_value(self, str1):
        return self.__get_bit(self.__hash1(str1)) and self.__get_bit(self.__hash2(str1))
