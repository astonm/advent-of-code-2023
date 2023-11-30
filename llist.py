# modified from https://dbader.org/blog/python-linked-list
from time import time


class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"<Node: {self.data}>"


class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __repr__(self):
        return repr(list(self))

    def walk_from(self, node, reversed=False):
        curr = node
        while True:
            yield curr
            curr = curr.next if not reversed else curr.prev
            if curr == node:
                break

    def __iter__(self):
        return self.walk_from(self.head)

    def reversed(self):
        return self.walk_from(self.tail, reversed=True)

    def values(self):
        return [node.data for node in self]

    def append(self, data):
        node = Node(data=data, prev=self.tail, next=self.head)
        if self.head is None:
            self.head = node
            self.tail = node

        self.tail.next = node
        self.head.prev = node
        self.tail = node
        return node

    def insert_after(self, target, node):
        node.next = target.next
        node.prev = target
        target.next.prev = node
        target.next = node

    def remove_elem(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        if node is self.head:
            self.head = node.next
        if node is self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = None
        return node
