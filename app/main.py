from typing import Any, Optional


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
        self.table: list[Optional[Node]] = [None] * self.max_capacity

    @staticmethod
    def get_hash(key: str) -> int:
        # value = key
        # if not isinstance(key, str|int|float):
        #     value = str(key)
        #
        # hash_value = 0
        #
        # for index, char in enumerate(value):
        #     hash_value += (ord(char) * (index + 1)) * 7

        hash_value = hash(key)

        return int(hash_value)

    def rebuild_table(self) -> None:
        self.max_capacity *= self.enlarger
        self.threshold = int(self.max_capacity * 0.7)
        old_table = self.table
        self.table: list[Optional[Node]] = [None] * self.max_capacity
        self.current_capacity = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def get_index(self, key: Any) -> int:
        return int(self.get_hash(key) % self.max_capacity)

    def add_new(self, index: int, key: Any, value: Any) -> None:
        self.table[index] = Node(key, value)
        self.current_capacity += 1

    def get_empty_position(self, index: int) -> int:
        start_index = index
        while True:
            if self.table[index] is None:
                return index
            elif self.table[index] is not None:
                index += 1
            if index >= self.max_capacity:
                index = 0
            if index == start_index:
                raise Exception("Dictionary is full")

    def __setitem__(self, key: Any, value: Any) -> Any:
        index = self.get_index(key)
        if (self.table[index] is None
                and self.current_capacity < self.threshold):
            self.add_new(index, key, value)
        elif self.current_capacity >= self.threshold:
            self.rebuild_table()
            index = self.get_index(key)
            self.add_new(index, key, value)
        elif self.table[index] is not None and self.table[index].key == key:
            self.table[index].value = value
        elif self.table[index] is not None:
            index = self.get_empty_position(index)
            self.add_new(index, key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        if self.table[index].key == key:
            return self.table[index].value
        else:
            while True:
                if self.table[index] is None:
                    raise KeyError("missing_key")
                if self.table[index].key == key:
                    return self.table[index].value
                index += 1
                if index >= self.max_capacity:
                    index = 0

    def __len__(self) -> int:
        return self.current_capacity
