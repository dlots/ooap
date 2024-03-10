#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PushStatus {
    NIL,    // never called push()
    OK,     // last push() call was successful
    ERROR   // last push() called on empty stack
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PopStatus {
    NIL,    // never called pop()
    OK,     // last pop() call was successful
    ERROR   // last pop() called on empty stack
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PeekStatus {
    NIL,    // never called peek()
    OK,     // last peek() call returned correct value
    ERROR   // last peek() called on empty stack
}

const DEFAULT_UPPER_BOUND: usize = 32;

// Definition of Abstract Data Type "BoundedStack"
pub trait BoundedStack<T> {
    /**
     * Constructors
    **/
    // Post-condition: a new empty stack with a default upper bound is created
    fn new() -> Self;

    // Post-condition: a new empty stack with a specified upper bound is created
    fn new_with_upper_bound(upper_bound: usize) -> Self;

    /**
     * Commands
    **/
    // Pre-condition: the stack is not full
    // Post-condition: a new value is added into the stack
    fn push(&mut self, value: T);

    // Pre-condition: the stack is not empty
    // Post-condition: the top element is removed from the stack
    fn pop(&mut self);

    // Post-condition: the stack is empty, command statuses are reset
    fn clear(&mut self);

    /**
     * Queries
    **/
    // Pre-condition: the stack is not empty
    fn peek(&mut self) -> Option<T>;

    fn size(&self) -> usize;

    /**
     * Status queries
    **/
    fn get_push_status(&self) -> PushStatus;
    fn get_pop_status(&self) -> PopStatus;
    fn get_peek_status(&self) -> PeekStatus;
}

pub struct BoundedStackImpl<T> {
    stack: Vec<T>,
    const_upper_bound: usize,
    push_status: PushStatus,
    pop_status: PopStatus,
    peek_status: PeekStatus,
}

impl <T: Copy> BoundedStack<T> for BoundedStackImpl<T> {
    fn new() -> Self {
        Self::new_with_upper_bound(DEFAULT_UPPER_BOUND)
    }

    fn new_with_upper_bound(upper_bound: usize) -> Self {
        BoundedStackImpl {
            stack: Vec::new(),
            const_upper_bound: upper_bound,
            push_status: PushStatus::NIL,
            pop_status: PopStatus::NIL,
            peek_status: PeekStatus::NIL
        }
    }

    fn push(&mut self, value: T) {
        if self.size() >= self.const_upper_bound {
            self.push_status = PushStatus::ERROR;
            return;
        }
        self.stack.push(value);
        self.push_status = PushStatus::OK;
    }

    fn pop(&mut self) {
        let size = self.size();
        if size <= 0 {
            self.pop_status = PopStatus::ERROR;
            return;
        }
        self.stack.pop();
        self.pop_status = PopStatus::OK;
    }

    fn clear(&mut self) {
        self.stack = Vec::new();
        self.push_status = PushStatus::NIL;
        self.pop_status = PopStatus::NIL;
        self.peek_status = PeekStatus::NIL;
    }

    fn peek(&mut self) -> Option<T> {
        if self.size() <= 0 {
            self.peek_status = PeekStatus::ERROR;
            return None;
        }
        self.peek_status = PeekStatus::OK;
        Some(self.stack[self.size() - 1])
    }

    fn size(&self) -> usize {
        self.stack.len()
    }

    fn get_push_status(&self) -> PushStatus {
        self.push_status
    }

    fn get_pop_status(&self) -> PopStatus {
        self.pop_status
    }

    fn get_peek_status(&self) -> PeekStatus {
        self.peek_status
    }
}

#[cfg(test)]
mod test {
    use crate::bounded_stack::*;

    fn assert_clear<T, U: BoundedStack<T>>(stack: &U) {
        assert_eq!(stack.size(), 0);
        assert_eq!(stack.get_push_status(), PushStatus::NIL);
        assert_eq!(stack.get_pop_status(), PopStatus::NIL);
        assert_eq!(stack.get_peek_status(), PeekStatus::NIL);
    }

    #[test]
    fn test_new() {
        let stack: BoundedStackImpl<i64> = BoundedStack::<i64>::new();
        assert_eq!(stack.const_upper_bound, DEFAULT_UPPER_BOUND);
        assert_clear(&stack);
    }

    #[test]
    fn test_new_with_upper_bound() {
        let upper_bound = 42;
        let stack: BoundedStackImpl<i64> = BoundedStack::<i64>::new_with_upper_bound(upper_bound);
        assert_eq!(stack.const_upper_bound, upper_bound);
        assert_clear(&stack);
    }

    #[test]
    fn test_commands_and_queries() {
        let mut stack: BoundedStackImpl<i64> = BoundedStack::<i64>::new();
        for i in 1..=DEFAULT_UPPER_BOUND {
            let value = i as i64;
            stack.push(value);
            assert_eq!(stack.get_push_status(), PushStatus::OK);
            assert_eq!(stack.size(), i);
            assert_eq!(stack.peek().unwrap(), value);
            assert_eq!(stack.get_peek_status(), PeekStatus::OK);
        }
        stack.push(1);
        assert_eq!(stack.get_push_status(), PushStatus::ERROR);
        assert_eq!(stack.size(), DEFAULT_UPPER_BOUND);
        assert_eq!(stack.peek().unwrap(), DEFAULT_UPPER_BOUND as i64);
        assert_eq!(stack.get_peek_status(), PeekStatus::OK);
        for i in (0..=DEFAULT_UPPER_BOUND - 1).rev() {
            let value = i as i64;
            stack.pop();
            assert_eq!(stack.get_pop_status(), PopStatus::OK);
            assert_eq!(stack.size(), i);
            if i == 0 {
                break;
            }
            assert_eq!(stack.peek().unwrap(), value);
            assert_eq!(stack.get_peek_status(), PeekStatus::OK);
        }
        stack.pop();
        assert_eq!(stack.get_pop_status(), PopStatus::ERROR);
        assert_eq!(stack.size(), 0);
        assert_eq!(stack.peek(), None);
        assert_eq!(stack.get_peek_status(), PeekStatus::ERROR);
    }
}