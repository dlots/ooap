import unittest
from dynamic_array import DynArrayImpl, SetCursorStatus, GetStatus, InsertStatus, RemoveStatus


class MyTestCase(unittest.TestCase):
    def test_empty(self):
        pass

    def test_append_within_capacity(self):
        array = DynArrayImpl()
        array.append(0)
        size = len(array)
        self.assertEqual(size, 1)
        for i in range(1, DynArrayImpl.DEFAULT_CAPACITY):
            array.append(i)
            array.set_cursor(i)
            self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.Ok)
            self.assertEqual(array.get_capacity(), DynArrayImpl.DEFAULT_CAPACITY)
            self.assertEqual(array.get(), i)
            self.assertEqual(array.get_get_status(), GetStatus.Ok)
            size += 1
            self.assertEqual(array.len(), size)

    def test_insertion_within_capacity(self):
        array = DynArrayImpl()
        array.append(0)
        size = len(array)
        self.assertEqual(size, 1)
        for i in range(1, DynArrayImpl.DEFAULT_CAPACITY):
            array.insert(i)
            self.assertEqual(array.get_insert_status(), InsertStatus.Ok)
            self.assertEqual(array.get_capacity(), DynArrayImpl.DEFAULT_CAPACITY)
            self.assertEqual(array.get(), i)
            self.assertEqual(array.get_get_status(), GetStatus.Ok)
            size += 1
            self.assertEqual(array.len(), size)

    def test_insertion_exceeding_capacity(self):
        array = DynArrayImpl()
        size = len(array)
        for i in range(DynArrayImpl.DEFAULT_CAPACITY):
            size += 1
            array.append(i)
        array.insert(123)
        self.assertEqual(array.get_insert_status(), InsertStatus.Ok)
        self.assertEqual(array.get_capacity(), DynArrayImpl.RESIZE_UP_RATE * DynArrayImpl.DEFAULT_CAPACITY)
        self.assertEqual(array.get(), 123)
        self.assertEqual(array.get_get_status(), GetStatus.Ok)
        self.assertEqual(array.len(), size + 1)

    def test_out_of_bound(self):
        array = DynArrayImpl()
        array.set_cursor(-1)
        self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.Empty)
        array.set_cursor(0)
        self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.Empty)
        array.append(0)
        array.set_cursor(-1)
        self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.OutOfBounds)
        array.set_cursor(0)
        self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.Ok)
        array.set_cursor(1)
        self.assertEqual(array.get_set_cursor_status(), SetCursorStatus.OutOfBounds)

    def test_deletion_no_resize(self):
        array = DynArrayImpl()
        for i in range(32):
            array.append(i)
        self.assertEqual(array.len(), 32)
        self.assertEqual(array.get_capacity(), 32)
        array.remove()
        self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
        self.assertEqual(array.len(), 31)
        self.assertEqual(array.get_capacity(), 32)
        self.assertEqual(array.get(), 1)
        self.assertEqual(array.get_get_status(), GetStatus.Ok)

    def test_deletion_with_resize(self):
        array = DynArrayImpl()
        for i in range(17):
            array.append(i)
        self.assertEqual(array.len(), 17)
        self.assertEqual(array.get_capacity(), 32)
        array.remove()
        self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
        array.remove()
        self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
        self.assertEqual(array.len(), 15)
        self.assertEqual(array.get_capacity(), 21)
        self.assertEqual(array.get(), 2)
        self.assertEqual(array.get_get_status(), GetStatus.Ok)

    def test_deletion_minimal_capacity(self):
        array = DynArrayImpl()
        for i in range(17):
            array.append(i)
        self.assertEqual(array.len(), 17)
        self.assertEqual(array.get_capacity(), 32)
        array.remove()
        self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
        self.assertEqual(array.len(), 16)
        self.assertEqual(array.get_capacity(), 32)
        array.remove()
        self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
        self.assertEqual(array.len(), 15)
        self.assertEqual(array.get_capacity(), 21)
        self.assertEqual(array.get(), 2)
        self.assertEqual(array.get_get_status(), GetStatus.Ok)
        for i in range(4):
            array.remove()
            self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
            self.assertEqual(array.len(), 14 - i)
            self.assertEqual(array.get_capacity(), 21)
        for i in range(11):
            array.remove()
            self.assertEqual(array.get_remove_status(), RemoveStatus.Ok)
            self.assertEqual(array.len(), 10 - i)
            self.assertEqual(array.get_capacity(), 16)


if __name__ == '__main__':
    unittest.main()
