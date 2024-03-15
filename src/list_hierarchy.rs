use std::cell::{RefCell};
use std::rc::{Rc, Weak};

// ====== Status definitions ======

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum HeadStatus {
    Nil,    // never called head()
    Ok,     // last head() call was successful
    Empty,  // last head() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum TailStatus {
    Nil,    // never called tail()
    Ok,     // last tail() call was successful
    Empty,  // last tail() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum LeftStatus {
    Nil,    // never called left()
    Ok,     // last left() call was successful
    Empty,  // last left() called on empty list
    NoLeft  // last left() called when current node had no left neighbor
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum RightStatus {
    Nil,    // never called right()
    Ok,     // last right() call was successful
    Empty,  // last right() called on empty list
    NoRight  // last right() called when current node had no right neighbor
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PutLeftStatus {
    Nil,    // never called put_left()
    Ok,     // last put_left() call was successful
    Empty,  // last put_left() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PutRightStatus {
    Nil,    // never called put_right()
    Ok,     // last put_right() call was successful
    Empty,  // last put_right() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum RemoveStatus {
    Nil,    // never called remove()
    Ok,     // last remove() call was successful
    Empty,  // last remove() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum ReplaceStatus {
    Nil,    // never called replace()
    Ok,     // last replace() call was successful
    Empty,  // last replace() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum GetStatus {
    Nil,    // never called get()
    Ok,     // last get() call was successful
    Empty,  // last get() called on empty list
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum FindStatus {
    Nil,      // never called find()
    Ok,       // last find() call was successful
    Empty,    // last find() called on empty list
    NotFound  // last find() did not found a value
}

// ====== Lists hierarchy definition ======

/**
 * Definition of Abstract Data Type "ParentList"
 **/
pub trait ParentList<T> {
    // ====== Constructors ======
    // Post-condition: a new empty list is created, the cursor is not defined
    fn new() -> Self;

    // ====== Commands ======
    // Pre-condition: the list is not empty
    // Post-condition: the cursor points to the head of the list if exists
    fn head(&mut self);

    // Pre-condition: the list is not empty
    // Post-condition: the cursor points to the tail of the list if exists
    fn tail(&mut self);

    // Pre-condition: the list is not empty and the next node exists
    // Post-condition: the cursor points to the next node
    fn right(&mut self);

    // Pre-condition: the list is not empty
    // Post-condition: a new node is inserted after the current node
    // If the list was empty, the cursor points to the new node
    fn put_left(&mut self, value: T);

    // Pre-condition: the list is not empty
    // Post-condition: a new node is inserted after the current node
    // If the list was empty, the cursor points to the new node
    fn put_right(&mut self, value: T);

    // Pre-condition: the list is not empty
    // Post-condition: current node is deleted, the cursor points to the next
    // node if it exists, or to the previous node if it exists
    fn remove(&mut self);

    // Post-condition: all nodes are deleted. The cursor is not defined.
    fn clear(&mut self);

    // Post-condition: a new node is inserted at the end of the list
    // If the list was empty, the cursor points to a new node.
    fn add_tail(&mut self, value: T);

    // Pre-condition: the list is not empty
    // Post-condition: the value of the current node is updated
    fn replace(&mut self, value: T);

    // Post-condition: the cursor points to the node with the specified
    // value if such node is found after the current node
    fn find(&mut self, value: &T) where T: PartialEq;

    // Post-condition: all nodes with specified value are removed from the list
    fn remove_all(&mut self, value: &T) where T: PartialEq;


    // ====== Queries ======
    // Pre-condition: the list is not empty
    fn get(&mut self) -> Option<Rc<T>>;

    fn size(&self) -> usize;

    fn is_head(&self) -> bool;

    fn is_tail(&self) -> bool;

    fn is_value(&self) -> bool;

    // ====== Status queries ======
    fn get_head_status(&self) -> HeadStatus;
    fn get_tail_status(&self) -> TailStatus;
    fn get_right_status(&self) -> RightStatus;
    fn get_put_left_status(&self) -> PutLeftStatus;
    fn get_put_right_status(&self) -> PutRightStatus;
    fn get_remove_status(&self) -> RemoveStatus;
    fn get_replace_status(&self) -> ReplaceStatus;
    fn get_get_status(&self) -> GetStatus;
    fn get_find_status(&self) -> FindStatus;
}

/**
 * Definition of Abstract Data Type "LinkedList"
**/
trait LinkedList<T>: ParentList<T> {
    // No new methods
}

/**
 * Definition of Abstract Data Type "TwoWayList"
**/
trait TwoWayList<T> : ParentList<T> {
    // Pre-condition: the list is not empty and the previous node exists
    // Post-condition: the cursor points to the previous node
    fn left(&mut self);

    fn get_left_status(&self) -> LeftStatus;
}

// ====== Implementations ======

struct ListNode<T> {
    value: RefCell<Rc<T>>,
    next: Option<Rc<RefCell<ListNode<T>>>>,
    previous: Option<Weak<RefCell<ListNode<T>>>>
}

struct ParentListImpl<T> {
    head: Option<Rc<RefCell<ListNode<T>>>>,
    tail: Option<Weak<RefCell<ListNode<T>>>>,
    cursor: Option<Weak<RefCell<ListNode<T>>>>,
    size: usize,
    head_status: HeadStatus,
    tail_status: TailStatus,
    right_status: RightStatus,
    put_left_status: PutLeftStatus,
    put_right_status: PutRightStatus,
    remove_status: RemoveStatus,
    replace_status: ReplaceStatus,
    get_status: GetStatus,
    find_status: FindStatus,
}

impl<T> ParentList<T> for ParentListImpl<T> {
    fn new() -> Self {
        ParentListImpl {
            head: None,
            tail: None,
            cursor: None,
            size: 0,
            head_status: HeadStatus::Nil,
            tail_status: TailStatus::Nil,
            right_status: RightStatus::Nil,
            put_left_status: PutLeftStatus::Nil,
            put_right_status: PutRightStatus::Nil,
            remove_status: RemoveStatus::Nil,
            replace_status: ReplaceStatus::Nil,
            get_status: GetStatus::Nil,
            find_status: FindStatus::Nil
        }
    }

    fn head(&mut self) {
        if self.size == 0 {
            self.head_status = HeadStatus::Empty;
            return;
        }

        let Some(head_rc) = &self.head else {
            panic!("head(): Head is None but self.size > 0");
        };

        self.cursor = Some(Rc::downgrade(head_rc));
        self.head_status = HeadStatus::Ok;
    }

    fn tail(&mut self) {
        if self.size == 0 {
            self.tail_status = TailStatus::Empty;
            return;
        }

        self.cursor = self.tail.clone();
        self.tail_status = TailStatus::Ok;
    }

    fn right(&mut self) {
        if self.size == 0 {
            self.right_status = RightStatus::Empty;
            return;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("right(): Cursor is None but self.size > 0");
        };

        if let Some(next_rc) = &cursor_rc.borrow().next {
            self.cursor = Some(Rc::downgrade(next_rc));
            self.right_status = RightStatus::Ok;
            return;
        }

        self.right_status = RightStatus::NoRight;
    }

    fn put_left(&mut self, value: T) {
        if self.size == 0 {
            self.put_left_status = PutLeftStatus::Empty;
            return;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("put_left(): Cursor is None but self.size > 0");
        };

        let new_node = Rc::new(RefCell::new(ListNode {
            value: RefCell::new(Rc::new(value)),
            next: Some(cursor_rc.clone()),
            previous: None
        }));
        cursor_rc.borrow_mut().previous = Some(Rc::downgrade(&new_node));
        if let Some(previous_rc) = cursor_rc.borrow().previous.clone().and_then(|weak| weak.upgrade()) {
            // Current node is not head
            new_node.borrow_mut().previous = Some(Rc::downgrade(&previous_rc));
            previous_rc.borrow_mut().next = Some(new_node);
        } else {
            self.head = Some(new_node);
        }

        self.size += 1;
        self.put_left_status = PutLeftStatus::Ok;
    }

    fn put_right(&mut self, value: T) {
        if self.size == 0 {
            self.put_right_status = PutRightStatus::Empty;
            return;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("put_right(): size > 0 but cursor is None");
        };

        let new_node = Rc::new(RefCell::new(ListNode {
            value: RefCell::new(Rc::new(value)),
            next: None,
            previous: Some(Rc::downgrade(&cursor_rc))
        }));
        cursor_rc.borrow_mut().next = Some(new_node.clone());
        if let Some(next_rc) = cursor_rc.borrow().next.clone() {
            // Current node is not tail
            next_rc.borrow_mut().previous = Some(Rc::downgrade(&new_node));
            new_node.borrow_mut().next = Some(next_rc);
        } else {
            // Current node is tail
            self.tail = Some(Rc::downgrade(&new_node));
        }

        self.size += 1;
        self.put_right_status = PutRightStatus::Ok;
    }

    fn remove(&mut self) {
        if self.size == 0 {
            self.remove_status = RemoveStatus::Empty;
            return;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("remove(): size > 0 but cursor is None");
        };

        if let Some(previous_rc) = cursor_rc.borrow().previous.clone().and_then(|weak| weak.upgrade()) {
            // Current node is not head
            previous_rc.borrow_mut().next = cursor_rc.borrow().next.clone();
        } else {
            // Current node is head
            self.head = cursor_rc.borrow().next.clone();
        }

        if let Some(next_rc) = cursor_rc.borrow().next.clone() {
            // Current node is not tail
            next_rc.borrow_mut().previous = cursor_rc.borrow().previous.clone();
        } else {
            // Current node is tail
            self.tail = cursor_rc.borrow().previous.clone();
        }

        cursor_rc.borrow_mut().previous = None;
        cursor_rc.borrow_mut().next = None;

        self.size -= 1;
        self.remove_status = RemoveStatus::Ok;
    }

    fn clear(&mut self) {
        self.head = None;
        self.tail = None;
        self.cursor = None;
        self.size = 0;
        self.head_status = HeadStatus::Nil;
        self.tail_status = TailStatus::Nil;
        self.right_status = RightStatus::Nil;
        self.put_left_status = PutLeftStatus::Nil;
        self.put_right_status = PutRightStatus::Nil;
        self.remove_status = RemoveStatus::Nil;
        self.replace_status = ReplaceStatus::Nil;
        self.get_status = GetStatus::Nil;
        self.find_status = FindStatus::Nil;
    }

    fn add_tail(&mut self, value: T) {
        self.size += 1;

        let new_value = Rc::new(RefCell::new(ListNode{
            value: RefCell::new(Rc::new(value)),
            next: None,
            previous: None
        }));

        if self.size == 1 {
            self.head = Some(new_value.clone());
        } else {
            let Some(tail_rc) = self.tail.clone().and_then(|weak| weak.upgrade()) else {
                panic!("add_tail(): size > 1 but tail is None");
            };
            new_value.borrow_mut().previous = self.tail.clone();
            tail_rc.borrow_mut().next = Some(new_value.clone());
        }

        self.tail = Some(Rc::downgrade(&new_value));
    }

    fn replace(&mut self, value: T) {
        if self.size == 0 {
            self.replace_status = ReplaceStatus::Empty;
            return;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("replace(): size > 0 but cursor is None");
        };

        *(cursor_rc.borrow().value.borrow_mut()) = Rc::new(value);
        self.replace_status = ReplaceStatus::Ok;
    }

    fn find(&mut self, value: &T) where T: PartialEq {
        if self.size == 0 {
            self.find_status = FindStatus::Empty;
        }

        let Some(current_rc) =  self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("find(): size > 0 but cursor is None");
        };

        let mut next_opt = current_rc.borrow().next.clone();
        while let Some(next_rc) = next_opt {
            if **(next_rc.borrow().value.borrow()) == *value {
                self.cursor = Some(Rc::downgrade(&next_rc));
                self.find_status = FindStatus::Ok;
                return;
            }
            next_opt = next_rc.borrow().next.clone();
        }

        self.find_status = FindStatus::NotFound;
    }

    fn remove_all(&mut self, value: &T) where T: PartialEq {
        if self.size == 0 {
            return;
        }

        self.find(value);
        while self.find_status == FindStatus::Ok {
            self.remove();
            if self.remove_status != RemoveStatus::Ok {
                panic!("Found the node, but couldn't remove it, error: {:?}", self.remove_status);
            }
            self.find(value);
        }
    }

    fn get(&mut self) -> Option<Rc<T>> {
        if self.size == 0 {
            self.get_status = GetStatus::Empty;
            return None;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("get(): Cursor is none but list is not empty");
        };

        self.get_status = GetStatus::Ok;
        let value_rc = cursor_rc.borrow().value.borrow().clone();
        Some(value_rc)
    }

    fn size(&self) -> usize {
        self.size
    }

    fn is_head(&self) -> bool {
        if self.size == 0 {
            return false;
        }

        let Some(cursor_rc) = self.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("is_head(): size > 0 but cursor is None");
        };

        let Some(head_rc) = &self.head else {
            panic!("is_head(): size > 0 but head is None");
        };

        Rc::ptr_eq(&cursor_rc, head_rc)
    }

    fn is_tail(&self) -> bool {
        if self.size == 0 {
            return false;
        }

        let Some(cursor_weak) = &self.cursor else {
            panic!("is_tail(): size > 0 but cursor is None");
        };

        let Some(tail_weak) = &self.tail else {
            panic!("is_tail(): size > 0 but head is None");
        };

        Weak::ptr_eq(cursor_weak, tail_weak)
    }

    fn is_value(&self) -> bool {
        self.size == 0
    }

    fn get_head_status(&self) -> HeadStatus {
        self.head_status
    }

    fn get_tail_status(&self) -> TailStatus {
        self.tail_status
    }

    fn get_right_status(&self) -> RightStatus {
        self.right_status
    }

    fn get_put_left_status(&self) -> PutLeftStatus {
        self.put_left_status
    }

    fn get_put_right_status(&self) -> PutRightStatus {
        self.put_right_status
    }

    fn get_remove_status(&self) -> RemoveStatus {
        self.remove_status
    }

    fn get_replace_status(&self) -> ReplaceStatus {
        self.replace_status
    }

    fn get_get_status(&self) -> GetStatus {
        self.get_status
    }

    fn get_find_status(&self) -> FindStatus {
        self.find_status
    }
}

struct LinkedListImpl<T> {
    delegate_list: ParentListImpl<T>
}

impl<T> LinkedList<T> for LinkedListImpl<T> {
    // No new methods
}

impl<T> ParentList<T> for LinkedListImpl<T> {
    fn new() -> Self {
        LinkedListImpl {
            delegate_list: ParentListImpl::<T>::new()
        }
    }

    fn head(&mut self) {
        self.delegate_list.head()
    }

    fn tail(&mut self) {
        self.delegate_list.tail()
    }

    fn right(&mut self) {
        self.delegate_list.right()
    }

    fn put_left(&mut self, value: T) {
        self.delegate_list.put_left(value)
    }

    fn put_right(&mut self, value: T) {
        self.delegate_list.put_right(value)
    }

    fn remove(&mut self) {
        self.delegate_list.remove()
    }

    fn clear(&mut self) {
        self.delegate_list.clear()
    }

    fn add_tail(&mut self, value: T) {
        self.delegate_list.add_tail(value)
    }

    fn replace(&mut self, value: T) {
        self.delegate_list.replace(value)
    }

    fn find(&mut self, value: &T) where T: PartialEq {
        self.delegate_list.find(value)
    }

    fn remove_all(&mut self, value: &T) where T: PartialEq {
        self.delegate_list.remove_all(value)
    }

    fn get(&mut self) -> Option<Rc<T>> {
        self.delegate_list.get()
    }

    fn size(&self) -> usize {
        self.delegate_list.size()
    }

    fn is_head(&self) -> bool {
        self.delegate_list.is_head()
    }

    fn is_tail(&self) -> bool {
        self.delegate_list.is_tail()
    }

    fn is_value(&self) -> bool {
        self.delegate_list.is_value()
    }

    fn get_head_status(&self) -> HeadStatus {
        self.delegate_list.get_head_status()
    }

    fn get_tail_status(&self) -> TailStatus {
        self.delegate_list.get_tail_status()
    }

    fn get_right_status(&self) -> RightStatus {
        self.delegate_list.get_right_status()
    }

    fn get_put_left_status(&self) -> PutLeftStatus {
        self.delegate_list.get_put_left_status()
    }

    fn get_put_right_status(&self) -> PutRightStatus {
        self.delegate_list.get_put_right_status()
    }

    fn get_remove_status(&self) -> RemoveStatus {
        self.delegate_list.get_remove_status()
    }

    fn get_replace_status(&self) -> ReplaceStatus {
        self.delegate_list.get_replace_status()
    }

    fn get_get_status(&self) -> GetStatus {
        self.delegate_list.get_get_status()
    }

    fn get_find_status(&self) -> FindStatus {
        self.delegate_list.get_find_status()
    }
}

struct DoublyLinkedListImpl<T> {
    delegate_list: ParentListImpl<T>,
    left_status: LeftStatus
}

impl<T> TwoWayList<T> for DoublyLinkedListImpl<T> {
    fn left(&mut self) {
        let delegate = &mut self.delegate_list;

        if delegate.size == 0 {
            self.left_status = LeftStatus::Empty;
            return;
        }

        let Some(cursor_rc) = delegate.cursor.clone().and_then(|weak| weak.upgrade()) else {
            panic!("left(): Cursor is None but self.size > 0");
        };

        if let Some(next_rc) = &cursor_rc.borrow().next {
            delegate.cursor = Some(Rc::downgrade(next_rc));
            self.left_status = LeftStatus::Ok;
            return;
        }

        self.left_status = LeftStatus::NoLeft;
    }

    fn get_left_status(&self) -> LeftStatus {
        self.left_status
    }
}

impl<T> ParentList<T> for DoublyLinkedListImpl<T> {
    fn new() -> Self {
        DoublyLinkedListImpl {
            delegate_list: ParentListImpl::<T>::new(),
            left_status: LeftStatus::Nil
        }
    }

    fn head(&mut self) {
        self.delegate_list.head()
    }

    fn tail(&mut self) {
        self.delegate_list.tail()
    }

    fn right(&mut self) {
        self.delegate_list.right()
    }

    fn put_left(&mut self, value: T) {
        self.delegate_list.put_left(value)
    }

    fn put_right(&mut self, value: T) {
        self.delegate_list.put_right(value)
    }

    fn remove(&mut self) {
        self.delegate_list.remove()
    }

    fn clear(&mut self) {
        self.delegate_list.clear()
    }

    fn add_tail(&mut self, value: T) {
        self.delegate_list.add_tail(value)
    }

    fn replace(&mut self, value: T) {
        self.delegate_list.replace(value)
    }

    fn find(&mut self, value: &T) where T: PartialEq {
        self.delegate_list.find(value)
    }

    fn remove_all(&mut self, value: &T) where T: PartialEq {
        self.delegate_list.remove_all(value)
    }

    fn get(&mut self) -> Option<Rc<T>> {
        self.delegate_list.get()
    }

    fn size(&self) -> usize {
        self.delegate_list.size()
    }

    fn is_head(&self) -> bool {
        self.delegate_list.is_head()
    }

    fn is_tail(&self) -> bool {
        self.delegate_list.is_tail()
    }

    fn is_value(&self) -> bool {
        self.delegate_list.is_value()
    }

    fn get_head_status(&self) -> HeadStatus {
        self.delegate_list.get_head_status()
    }

    fn get_tail_status(&self) -> TailStatus {
        self.delegate_list.get_tail_status()
    }

    fn get_right_status(&self) -> RightStatus {
        self.delegate_list.get_right_status()
    }

    fn get_put_left_status(&self) -> PutLeftStatus {
        self.delegate_list.get_put_left_status()
    }

    fn get_put_right_status(&self) -> PutRightStatus {
        self.delegate_list.get_put_right_status()
    }

    fn get_remove_status(&self) -> RemoveStatus {
        self.delegate_list.get_remove_status()
    }

    fn get_replace_status(&self) -> ReplaceStatus {
        self.delegate_list.get_replace_status()
    }

    fn get_get_status(&self) -> GetStatus {
        self.delegate_list.get_get_status()
    }

    fn get_find_status(&self) -> FindStatus {
        self.delegate_list.get_find_status()
    }
}