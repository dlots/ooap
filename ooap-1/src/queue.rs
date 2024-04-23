#[derive(Debug, Copy, Clone, PartialEq)]
pub enum DequeueStatus {
    Nil,    // never called dequeue()
    Ok,     // last dequeue() call was successful
    Empty,  // last dequeue() called on empty queue
}

// ====== Definition of abstract data type "Queue" ======
pub trait Queue<T> {
    // Post-condition: a new empty queue is created
    fn new() -> Self;

    // Post-condition: a new value is added to the back of the queue
    fn enqueue(&mut self, value: T);

    // Pre-condition: the queue is not empty
    // Post-condition: a value is removed from the front of the queue
    fn dequeue(&mut self) -> Option<T>;

    fn len(&self) -> usize;

    fn get_dequeue_status(&self) -> DequeueStatus;
}

pub struct QueueImpl<T> {
    back_stack: Vec<T>,
    front_stack: Vec<T>,
    dequeue_status: DequeueStatus
}

impl<T> Queue<T> for QueueImpl<T> {
    fn new() -> Self {
        QueueImpl {
            back_stack: Vec::new(),
            front_stack: Vec::new(),
            dequeue_status: DequeueStatus::Nil
        }
    }

    fn enqueue(&mut self, value: T) {
        self.back_stack.push(value);
    }

    fn dequeue(&mut self) -> Option<T> {
        if self.len() == 0 {
            self.dequeue_status = DequeueStatus::Empty;
            return None;
        }

        self.dequeue_status = DequeueStatus::Ok;

        if self.front_stack.len() > 0 {
            return self.front_stack.pop();
        }

        while self.back_stack.len() > 1 {
            self.front_stack.push(self.back_stack.pop().unwrap());
        }

        self.back_stack.pop()
    }

    fn len(&self) -> usize {
        self.back_stack.len() + self.front_stack.len()
    }

    fn get_dequeue_status(&self) -> DequeueStatus {
        self.dequeue_status
    }
}

#[cfg(test)]
mod test {
    use crate::queue::*;

    #[test]
    fn test_queue() {
        let mut queue: QueueImpl<i64> = Queue::<i64>::new();
        assert_eq!(queue.len(), 0);
        assert_eq!(queue.get_dequeue_status(), DequeueStatus::Nil);
        assert_eq!(queue.dequeue(), None);
        assert_eq!(queue.get_dequeue_status(), DequeueStatus::Empty);

        let max = 100;
        let range = 1..max+1;

        for i in range.clone() {
            queue.enqueue(i);
            assert_eq!(queue.len(), i as usize);
        }

        for i in range {
            assert_eq!(queue.dequeue(), Some(i));
            assert_eq!(queue.get_dequeue_status(), DequeueStatus::Ok);
            assert_eq!(queue.len(), (max - i) as usize);
        }
    }
}