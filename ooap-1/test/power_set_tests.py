import unittest
import random
import string
from power_set import *


def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=25))


class TestHashTable(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHashTable, self).__init__(*args, **kwargs)
        self.strings = [generate_random_string() for _ in range(3000)]

    def test(self):
        table = PowerSet(30)
        strings = ['abc', 'afqewf', 'adsggqw', 'wghweghehw', 'qwgqewgqgqe']
        abcs = ['abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc']
        for string in strings:
            table.put(string)
            self.assertEqual(table.get_put_status(), ht.PutStatus.Ok)
            self.assertEqual(table.seek(string), True)
            self.assertEqual(table.get_seek_status(), ht.SeekStatus.Ok)
        for string in abcs:
            table.put(string)
            self.assertEqual(table.get_put_status(), ht.PutStatus.Exists)
            self.assertEqual(table.seek(string), True)
            self.assertEqual(table.get_seek_status(), ht.SeekStatus.Ok)
        strings = ['afqewf', 'adsggqw', 'wghweghehw', 'qwgqewgqgqe',]
        for string in strings:
            table.remove(string)
            self.assertEqual(table.get_remove_status(), ht.RemoveStatus.Ok)
            self.assertEqual(table.seek(string), False)
            self.assertEqual(table.get_seek_status(), ht.SeekStatus.Ok)
        table.remove('abc')
        self.assertEqual(table.get_remove_status(), ht.RemoveStatus.Ok)
        self.assertEqual(table.seek('abc'), False)
        self.assertEqual(table.get_seek_status(), ht.SeekStatus.Ok)
        for string in abcs:
            table.remove(string)
            self.assertEqual(table.get_remove_status(), ht.RemoveStatus.NotFound)
            self.assertEqual(table.seek(string), False)
            self.assertEqual(table.get_seek_status(), ht.SeekStatus.Ok)
        table.put('123')
        table.remove('abc')
        self.assertEqual(table.get_remove_status(), ht.RemoveStatus.NotFound)

    def test_intersection_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(1001, 2001):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.intersection(p_set2).size(), 0)

    def test_intersection_not_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(501, 1501):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.intersection(p_set2).size(), 500)

    def test_union_intersecting(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(501, 1501):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.union(p_set2).size(), 1500)

    def test_union_non_intersecting(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(1001, 1501):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.union(p_set2).size(), 1500)

    def test_union_self_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1001, 1501):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.union(p_set2).size(), 500)

    def test_union_param_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        self.assertEqual(p_set1.union(p_set2).size(), 1000)

    def test_difference_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
            self.assertEqual(p_set1.get_put_status(), ht.PutStatus.Ok)
        for i in range(1, 1001):
            p_set2.put(self.strings[i])
            self.assertEqual(p_set2.get_put_status(), ht.PutStatus.Ok)
        self.assertEqual(p_set1.difference(p_set2).size(), 0)

    def test_difference_not_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(501, 1001):
            p_set2.put(self.strings[i])
        self.assertEqual(p_set1.difference(p_set2).size(), 500)

    def test_is_subset_param_in_self(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(501, 1001):
            p_set2.put(self.strings[i])
        self.assertTrue(p_set1.is_subset(p_set2))

    def test_is_subset_self_in_param(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(501, 1001):
            p_set1.put(self.strings[i])
        for i in range(1, 1001):
            p_set2.put(self.strings[i])
        self.assertFalse(p_set1.is_subset(p_set2))

    def test_is_subset_intersecting(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        for i in range(1, 1001):
            p_set1.put(self.strings[i])
        for i in range(501, 1501):
            p_set2.put(self.strings[i])
        self.assertFalse(p_set1.is_subset(p_set2))

    def test_is_subset_both_empty(self):
        p_set1 = PowerSet(30)
        p_set2 = PowerSet(30)
        self.assertTrue(p_set1.is_subset(p_set2))


if __name__ == '__main__':
    unittest.main()