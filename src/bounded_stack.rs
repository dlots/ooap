#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PushStatus {
    Nil,    // never called push()
    Ok,     // last push() call was successful
    Error   // last push() called on empty stack
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PopStatus {
    Nil,    // never called pop()
    Ok,     // last pop() call was successful
    Error   // last pop() called on empty stack
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum PeekStatus {
    Nil,    // never called peek()
    Ok,     // last peek() call returned correct value
    Error   // last peek() called on empty stack
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
            push_status: PushStatus::Nil,
            pop_status: PopStatus::Nil,
            peek_status: PeekStatus::Nil
        }
    }

    fn push(&mut self, value: T) {
        if self.size() >= self.const_upper_bound {
            self.push_status = PushStatus::Error;
            return;
        }
        self.stack.push(value);
        self.push_status = PushStatus::Ok;
    }

    fn pop(&mut self) {
        let size = self.size();
        if size <= 0 {
            self.pop_status = PopStatus::Error;
            return;
        }
        self.stack.pop();
        self.pop_status = PopStatus::Ok;
    }

    fn clear(&mut self) {
        self.stack = Vec::new();
        self.push_status = PushStatus::Nil;
        self.pop_status = PopStatus::Nil;
        self.peek_status = PeekStatus::Nil;
    }

    fn peek(&mut self) -> Option<T> {
        if self.size() <= 0 {
            self.peek_status = PeekStatus::Error;
            return None;
        }
        self.peek_status = PeekStatus::Ok;
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
        assert_eq!(stack.get_push_status(), PushStatus::Nil);
        assert_eq!(stack.get_pop_status(), PopStatus::Nil);
        assert_eq!(stack.get_peek_status(), PeekStatus::Nil);
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
            assert_eq!(stack.get_push_status(), PushStatus::Ok);
            assert_eq!(stack.size(), i);
            assert_eq!(stack.peek().unwrap(), value);
            assert_eq!(stack.get_peek_status(), PeekStatus::Ok);
        }
        stack.push(1);
        assert_eq!(stack.get_push_status(), PushStatus::Error);
        assert_eq!(stack.size(), DEFAULT_UPPER_BOUND);
        assert_eq!(stack.peek().unwrap(), DEFAULT_UPPER_BOUND as i64);
        assert_eq!(stack.get_peek_status(), PeekStatus::Ok);
        for i in (0..=DEFAULT_UPPER_BOUND - 1).rev() {
            let value = i as i64;
            stack.pop();
            assert_eq!(stack.get_pop_status(), PopStatus::Ok);
            assert_eq!(stack.size(), i);
            if i == 0 {
                break;
            }
            assert_eq!(stack.peek().unwrap(), value);
            assert_eq!(stack.get_peek_status(), PeekStatus::Ok);
        }
        stack.pop();
        assert_eq!(stack.get_pop_status(), PopStatus::Error);
        assert_eq!(stack.size(), 0);
        assert_eq!(stack.peek(), None);
        assert_eq!(stack.get_peek_status(), PeekStatus::Error);
    }
}
