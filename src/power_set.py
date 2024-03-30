from abc import ABC, abstractmethod
import hash_table as ht


class AbstractPowerSet(ABC):
    @abstractmethod
    # Post-condition: a new set is created
    def __init__(self, capacity):
        pass

    """ Commands """

    # Pre-condition: table has a slot for value, the value is not None, value does not exist
    # Post-condition: a new value is added to a set, if collision is resolved successfully
    @abstractmethod
    def put(self, value):
        pass

    # Pre-condition: the value exists in the set, the value is not None
    # Post-condition: the value is removed from the set
    @abstractmethod
    def remove(self, value):
        pass

    """ Queries """

    # Return the number of elements
    @abstractmethod
    def size(self):
        pass

    # Pre-condition: the value to search is not None
    @abstractmethod
    def seek(self, value):
        pass

    @abstractmethod
    def intersection(self, other):
        pass

    @abstractmethod
    def union(self, other):
        pass

    @abstractmethod
    def difference(self, other):
        pass

    @abstractmethod
    def is_subset(self, other):
        pass

    """ Status queries """

    @abstractmethod
    def get_seek_status(self):
        pass

    @abstractmethod
    def get_put_status(self):
        pass

    @abstractmethod
    def get_remove_status(self):
        pass


class PowerSet(ht.HashTable, AbstractPowerSet):
    def __init__(self, capacity):
        super().__init__(capacity)

    def put(self, value):
        exists = self.seek(value)
        status = self.get_seek_status()
        if self.get_seek_status() == ht.SeekStatus.IsNone:
            self._put_status = ht.PutStatus.IsNone
            return status
        if exists:
            self._put_status = ht.PutStatus.Exists
            return
        super().put(value)

    def intersection(self, other):
        result = PowerSet(min(self.capacity, other.capacity))
        for bucket in self.data:
            if bucket is None:
                continue
            for entry in bucket:
                value, _ = entry
                if other.seek(value):
                    result.put(value)
        return result

    def add_all_to(self, other):
        for bucket in self.data:
            if bucket is None:
                continue
            for entry in bucket:
                value, _ = entry
                other.put(value)

    def union(self, other):
        result = PowerSet(self.capacity + other.capacity)
        self.add_all_to(result)
        other.add_all_to(result)
        return result

    def difference(self, other):
        result = PowerSet(max(self.capacity, other.capacity))
        self.add_all_to(result)
        for bucket in other.data:
            if bucket is None:
                continue
            for entry in bucket:
                value, _ = entry
                result.remove(value)
        return result

    def is_subset(self, other):
        for bucket in other.data:
            if bucket is None:
                continue
            for entry in bucket:
                value, _ = entry
                if not self.seek(value):
                    return False
        return True

