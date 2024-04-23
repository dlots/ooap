#[derive(Debug, Copy, Clone, PartialEq)]
pub enum SetCursorStatus {
    Nil,
    Ok,
    Empty,
    OutOfBounds,
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum GetStatus {
    Nil,
    Ok,
    Empty,
    OutOfBounds,
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum ReplaceStatus {
    Nil,
    Ok,
    Empty,
    OutOfBounds,
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum InsertStatus {
    Nil,
    Ok,
    Empty,
    OutOfBounds,
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum RemoveStatus {
    Nil,
    Ok,
    Empty,
    OutOfBounds,
}

pub trait DynArray<T> {
    fn new() -> Self;

    fn new_with_capacity(capacity: usize) -> Self;

    fn size(&self) -> usize;

    fn append(&mut self, value: T);

    fn set_cursor(&mut self, i: usize);

    // refs may be invalidated after resize...
    fn get<'a>(&mut self) -> Option<&'a T>;

    fn replace(&mut self, value: T);

    fn insert(&mut self, value: T);

    fn remove(&mut self);

    fn get_set_cursor_status(&self) -> SetCursorStatus;

    fn get_get_status(&self) -> GetStatus;

    fn get_replace_status(&self) -> ReplaceStatus;

    fn get_insert_status(&self) -> InsertStatus;

    fn get_remove_status(&self) -> RemoveStatus;
}

const DEFAULT_CAPACITY: usize = 16;

pub struct DynArrayImpl<T> {
    data: *mut T,
    size: usize,
    capacity: usize,
    minimal_capacity: usize,
    cursor: usize,
    set_cursor_status: SetCursorStatus,
    get_status: GetStatus,
    replace_status: ReplaceStatus,
    insert_status: InsertStatus,
    remove_status: RemoveStatus
}

impl<T> DynArrayImpl<T> {
    fn resize(&mut self, new_capacity: usize) {
        let new_layout = std::alloc::Layout::array::<T>(new_capacity).unwrap();
        let new_data = unsafe { std::alloc::alloc(new_layout) as *mut T };
        if new_data.is_null() {
            panic!("Failed to allocate memory for resizing");
        }
        unsafe {
            std::ptr::copy_nonoverlapping(self.data, new_data, self.size);
            std::alloc::dealloc(self.data as *mut u8, new_layout);
        }
        self.data = new_data;
        self.capacity = new_capacity;
    }
}

impl<T> Drop for DynArrayImpl<T> {
    fn drop(&mut self) {
        let layout = std::alloc::Layout::array::<T>(self.capacity).unwrap();
        unsafe {
            std::alloc::dealloc(self.data as *mut u8, layout);
        }
    }
}

// TODO: finish implementation. After resize references retrieved with get() will be invalidated.
// Can I raise a compile error in that case? Probably not? Panic? I need to turn in the assignment
// so this will be done later as an additional homework when I understand Rust better.

impl<T> DynArray<T> for DynArrayImpl<T> {
    fn new() -> Self {
        Self::new_with_capacity(DEFAULT_CAPACITY)
    }

    fn new_with_capacity(capacity: usize) -> Self {
        let layout = std::alloc::Layout::array::<T>(capacity).unwrap();
        let data = unsafe { std::alloc::alloc(layout) as *mut T };

        if data.is_null() {
            panic!("Failed to allocate memory");
        }

        DynArrayImpl {
            data,
            size: 0,
            capacity,
            minimal_capacity: capacity,
            cursor: 0,
            set_cursor_status: SetCursorStatus::Nil,
            get_status: GetStatus::Nil,
            replace_status: ReplaceStatus::Nil,
            insert_status: InsertStatus::Nil,
            remove_status: RemoveStatus::Nil
        }
    }

    fn size(&self) -> usize {
        self.size
    }

    fn append(&mut self, value: T) {
        todo!()
    }

    fn set_cursor(&mut self, i: usize) {
        if self.size == 0 {
            self.set_cursor_status = SetCursorStatus::Empty;
            return;
        }

        if i >= self.size {
            self.set_cursor_status = SetCursorStatus::OutOfBounds;
        }

        self.cursor = i;
        self.set_cursor_status = SetCursorStatus::Ok;
    }

    fn get<'a>(&mut self) -> Option<&'a T> {
        todo!()
    }

    fn replace(&mut self, value: T) {
        todo!()
    }

    fn insert(&mut self, value: T) {
        todo!()
    }

    fn remove(&mut self) {
        todo!()
    }

    fn get_set_cursor_status(&self) -> SetCursorStatus {
        self.set_cursor_status
    }

    fn get_get_status(&self) -> GetStatus {
        self.get_status
    }

    fn get_replace_status(&self) -> ReplaceStatus {
        self.replace_status
    }

    fn get_insert_status(&self) -> InsertStatus {
        self.insert_status
    }

    fn get_remove_status(&self) -> RemoveStatus {
        self.remove_status
    }
}
