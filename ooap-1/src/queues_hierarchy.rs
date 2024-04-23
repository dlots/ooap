use std::collections::VecDeque;

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum GetTailStatus {
    Nil,    // never called get_tail()
    Ok,     // last get_tail() call was successful
    Empty,  // last get_tail() called on empty queue
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum DequeueTailStatus {
    Nil,    // never called dequeue_tail()
    Ok,     // last dequeue_tail() call was successful
    Empty,  // last dequeue_tail() called on empty queue
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum GetHeadStatus {
    Nil,    // never called get_head()
    Ok,     // last get_head() call was successful
    Empty,  // last get_head() called on empty queue
}

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum DequeueHeadStatus {
    Nil,    // never called dequeue_head()
    Ok,     // last dequeue_head() call was successful
    Empty,  // last dequeue_head() called on empty queue
}

// ====== Definition of base type "ParentQueue" ======
pub trait ParentQueue<T> {
    // Post-condition: a new empty queue is created
    fn new() -> Self;

    // Post-condition: a new value is added to the back of the queue
    fn enqueue_tail(&mut self, value: T);

    // Pre-condition: the queue is not empty
    fn get_head(&mut self) -> Option<&T>;

    // Pre-condition: the queue is not empty
    // Post-condition: a value is removed from the front of the queue
    fn dequeue_head(&mut self);

    fn len(&self) -> usize;

    fn get_get_head_status(&self) -> GetHeadStatus;

    fn get_dequeue_head_status(&self) -> DequeueHeadStatus;
}

// ====== Definition of abstract data type "Queue ======
pub trait Queue<T>: ParentQueue<T> {
    fn new() -> Self;
}

// ====== Definition of abstract data type "Deque" ======
pub trait Deque<T>: ParentQueue<T> {
    fn new() -> Self;

    fn enqueue_head(&mut self, value: T);

    fn get_tail(&mut self) -> Option<&T>;

    fn dequeue_tail(&mut self);

    fn get_get_tail_status(&self) -> GetTailStatus;

    fn get_dequeue_tail_status(&self) -> DequeueTailStatus;
}

// ====== Implementations ======

pub struct ParentQueueImpl<T> {
    data: VecDeque<T>,
    get_head_status: GetHeadStatus,
    dequeue_head_status: DequeueHeadStatus
}

impl<T> ParentQueue<T> for ParentQueueImpl<T> {
    fn new() -> Self {
        ParentQueueImpl {
            data: VecDeque::<T>::new(),
            get_head_status: GetHeadStatus::Nil,
            dequeue_head_status: DequeueHeadStatus::Nil
        }
    }

    fn enqueue_tail(&mut self, value: T) {
        self.data.push_back(value)
    }

    fn get_head(&mut self) -> Option<&T> {
        if self.len() == 0 {
            self.get_head_status = GetHeadStatus::Empty;
            return None;
        }
        self.get_head_status = GetHeadStatus::Ok;
        self.data.front()
    }

    fn dequeue_head(&mut self) {
        if self.len() == 0 {
            self.dequeue_head_status = DequeueHeadStatus::Empty;
            return;
        }
        self.dequeue_head_status = DequeueHeadStatus::Ok;
        self.data.pop_front();
    }

    fn len(&self) -> usize {
        self.data.len()
    }

    fn get_get_head_status(&self) -> GetHeadStatus {
        self.get_head_status
    }

    fn get_dequeue_head_status(&self) -> DequeueHeadStatus {
        self.dequeue_head_status
    }
}

pub struct QueueImpl<T> {
    delegate_queue: ParentQueueImpl<T>
}

impl<T> Queue<T> for QueueImpl<T> {
    fn new() -> Self {
        ParentQueue::<T>::new()
    }
}

impl<T> ParentQueue<T> for QueueImpl<T> {
    fn new() -> Self {
        QueueImpl {
            delegate_queue: ParentQueueImpl::<T>::new()
        }
    }

    fn enqueue_tail(&mut self, value: T) {
        self.delegate_queue.enqueue_tail(value)
    }

    fn get_head(&mut self) -> Option<&T> {
        self.delegate_queue.get_head()
    }

    fn dequeue_head(&mut self) {
        self.delegate_queue.dequeue_head()
    }

    fn len(&self) -> usize {
        self.delegate_queue.len()
    }

    fn get_get_head_status(&self) -> GetHeadStatus {
        self.delegate_queue.get_get_head_status()
    }

    fn get_dequeue_head_status(&self) -> DequeueHeadStatus {
        self.delegate_queue.get_dequeue_head_status()
    }
}

pub struct DequeImpl<T> {
    delegate_deque: ParentQueueImpl<T>,
    get_tail_status: GetTailStatus,
    dequeue_tail_status: DequeueTailStatus
}

impl<T> Deque<T> for DequeImpl<T> {
    fn new() -> Self {
        ParentQueue::<T>::new()
    }

    fn enqueue_head(&mut self, value: T) {
        self.delegate_deque.data.push_front(value)
    }

    fn get_tail(&mut self) -> Option<&T> {
        if self.delegate_deque.len() == 0 {
            self.get_tail_status = GetTailStatus::Empty;
            return None;
        }
        self.get_tail_status = GetTailStatus::Ok;
        self.delegate_deque.data.back()
    }

    fn dequeue_tail(&mut self) {
        if self.delegate_deque.len() == 0 {
            self.dequeue_tail_status = DequeueTailStatus::Empty;
            return;
        }
        self.dequeue_tail_status = DequeueTailStatus::Ok;
        self.delegate_deque.data.pop_back();
    }

    fn get_get_tail_status(&self) -> GetTailStatus {
        self.get_tail_status
    }

    fn get_dequeue_tail_status(&self) -> DequeueTailStatus {
        self.dequeue_tail_status
    }
}

impl<T> ParentQueue<T> for DequeImpl<T> {
    fn new() -> Self {
        DequeImpl {
            delegate_deque: ParentQueueImpl::<T>::new(),
            get_tail_status: GetTailStatus::Nil,
            dequeue_tail_status: DequeueTailStatus::Nil
        }
    }

    fn enqueue_tail(&mut self, value: T) {
        self.delegate_deque.enqueue_tail(value)
    }

    fn get_head(&mut self) -> Option<&T> {
        self.delegate_deque.get_head()
    }

    fn dequeue_head(&mut self) {
        self.delegate_deque.dequeue_head()
    }

    fn len(&self) -> usize {
        self.delegate_deque.len()
    }

    fn get_get_head_status(&self) -> GetHeadStatus {
        self.delegate_deque.get_get_head_status()
    }

    fn get_dequeue_head_status(&self) -> DequeueHeadStatus {
        self.delegate_deque.get_dequeue_head_status()
    }
}

#[cfg(test)]
mod test {
    use crate::queues_hierarchy::*;

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