from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.max_capacity = 8
        self.threshold = int(self.max_capacity * 0.7)
        self.current_capacity = 0
        self.enlarger = 2
        self.table = [None] * self.max_capacity

    @staticmethod
    def get_hash(key: Any) -> int:
        return hash(key)

    def get_index(self, key: Any) -> int:
        return self.get_hash(key) % self.max_capacity

    def find_empty_slot(self, index: int) -> int:
        start_index = index
        while True:
            if self.table[index] is None:
                return index
            index = (index + 1) % self.max_capacity
            if index == start_index:
                raise Exception("Dictionary is full")

    def insert(self, index: int, key: Any, value: Any) -> None:
        self.table[index] = Node(key, value)
        self.current_capacity += 1

    def rebuild_table(self) -> None:
        self.max_capacity *= self.enlarger
        self.threshold = int(self.max_capacity * 0.7)
        old_table = self.table
        self.table = [None] * self.max_capacity
        self.current_capacity = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.current_capacity >= self.threshold:
            self.rebuild_table()

        index = self.get_index(key)
        if self.table[index] is None:
            self.insert(index, key, value)
        elif self.table[index].key == key:
            self.table[index].value = value
        else:
            index = self.find_empty_slot(index)
            self.insert(index, key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.max_capacity
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.current_capacity
