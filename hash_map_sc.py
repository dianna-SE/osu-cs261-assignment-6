# Name: Dianna Pham
# OSU Email:  phamdia@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 6 - HashMap (Portfolio Assignment): Separate Chaining
# Due Date: Aug 15, 2023
# Description: Implement methods within the HashMap class that integrates
#               proper separate chaining techniques.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method that updates the key-value pair in a hash map and any existing keys given will have their
        value replaced with the new one. Otherwise, the key-value pair is added into the hash map.

        Table resizes are doubled from its capacity and the load factor is greater than or equal to 1.0.
        """

        # resize if load factor is at or exceeds 1.0
        load_factor = self.table_load()

        if load_factor >= 1.0:
            double_capacity = self.get_capacity() * 2
            self.resize_table(double_capacity)

        # get hash value and its' index
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()  # index = hash % array_size

        # find the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # existing key -- replace value with new value
        for item in bucket:
            if item.key == key:
                bucket.remove(key)
                bucket.insert(key, value)
                return

        # key does not exist, add key-value pair into hash map
        bucket.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Method that simply returns how many empty buckets exist within the hash table.
        """
        # buckets are slots inside the hash table
        buckets = 0

        # traverse through the buckets
        for num in range(self._capacity):
            if self._buckets[num].length() == 0:
                buckets += 1

        return buckets

    def table_load(self) -> float:
        """
        Method that returns the load factor of the hash table.
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        Method that wipes out the contents in the hash map without changing the capacity.
        """
        self._buckets = DynamicArray()

        # set new linked lists to each bucket
        for items in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that changes the capacity of the hash table and rehashes existing key-value pairs into
        the new hash map.
        """

        if new_capacity < 1:
            return

        print("old capacity", new_capacity)
        # not prime, change to next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # prime, resize the hash map and create new hash map to new capacity
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # traverse through hash map
        for num in range(self._capacity):

            # if the length this bucket at this index is NOT empty, rehash key-value pairs
            if self._buckets[num].length():
                for item in self._buckets[num]:

                    # get hash value and its' index
                    hash_value = self._hash_function(item.key)
                    new_index = hash_value % new_capacity

                    # insert key-value pair at this index
                    new_hash_map._buckets[new_index].insert(item.key, item.value)

        # update new values of new hash map
        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity
        print("new capacity", self._capacity)


    def get(self, key: str):
        """
        Method that returns the value using the key and returns None if the key does not exist within
        the hash map.
        """
        # get the hash using key
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()  # index = hash % array_size

        # get the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # traverse through the bucket to find the key
        for item in bucket:
            if item.key == key:
                return item.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Method that returns True if there exists the key in the hash map and returns False if it does not
        (i.e., empty hash map).
        """
        # empty hash map
        if self._size == 0:
            return False

        # get hash value and its' index
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()  # index = hash % array_size

        # find the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # existing key -- replace value with new value
        for item in bucket:
            if item.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Method that simply removes the given key-value pair from the hash map.
        """
        # get hash value and its' index
        hash_value = self._hash_function(key)
        index = hash_value % self.get_capacity()  # index = hash % array_size

        # find the bucket (dynamic array) corresponding to the hash value
        bucket = self._buckets.get_at_index(index)

        # existing key -- replace value with new value
        for item in bucket:
            if item.key == key:
                bucket.remove(key)
                self._size -= 1

        if self._size < 0:
            self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that returns a dynamic array of indexes of tuple key-value pairs within the hash map
        in any key order.
        """
        keys_and_values = DynamicArray()

        # traverse through hash map and get the bucket
        for bucket in range(self._capacity):

            # bucket is not empty, append key-value pairs into dynamic array
            if self._buckets[bucket].length() != 0:

                for item in self._buckets[bucket]:
                    keys_and_values.append((item.key, item.value))

        return keys_and_values

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Method that takes in a dynamic array that is either sorted or unsorted and returns a tuple of
    a dynamic array that establishes the mode and frequency for the mode in O(n) runtime complexity.
    There can be multiple modes if they are the same frequencies.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap

    # recommended to use separate chaining hash map instance provided in the function's skeleton code.
    map = HashMap()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
