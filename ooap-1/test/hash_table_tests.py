import unittest
from hash_table import *


def test_real_size(test_case, table):
    real_size = 0
    for bucket in table.data:
        if bucket is None:
            continue
        for entry in bucket:
            _, count = entry
            real_size += count
    test_case.assertEqual(real_size, table.size())


class TestHashTable(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHashTable, self).__init__(*args, **kwargs)

    def test(self):
        table = HashTable(30)
        strings = ['abc', 'afqewf', 'adsggqw', 'wghweghehw', 'qwgqewgqgqe', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc',
                   'abc', 'abc', 'abc', 'abc', ]
        for string in strings:
            table.put(string)
            test_real_size(self, table)
            self.assertEqual(table.get_put_status(), PutStatus.Ok)
            self.assertEqual(table.seek(string), True, string)
            self.assertEqual(table.get_seek_status(), SeekStatus.Ok)
        strings = ['afqewf', 'adsggqw', 'wghweghehw', 'qwgqewgqgqe',]
        for string in strings:
            table.remove(string)
            test_real_size(self, table)
            self.assertEqual(table.get_remove_status(), RemoveStatus.Ok)
            self.assertEqual(table.seek(string), False)
            self.assertEqual(table.get_seek_status(), SeekStatus.Ok)
        strings = ['abc'] * 10
        for string in strings:
            table.remove(string)
            test_real_size(self, table)
            self.assertEqual(table.get_remove_status(), RemoveStatus.Ok)
            self.assertEqual(table.seek(string), True)
            self.assertEqual(table.get_seek_status(), SeekStatus.Ok)
        table.remove('abc')
        test_real_size(self, table)
        self.assertEqual(table.get_remove_status(), RemoveStatus.Ok)
        self.assertEqual(table.seek('abc'), False)
        self.assertEqual(table.get_seek_status(), SeekStatus.Ok)
        table.put('123')
        table.remove('abc')
        test_real_size(self, table)
        self.assertEqual(table.get_remove_status(), RemoveStatus.NotFound)


if __name__ == '__main__':
    unittest.main()