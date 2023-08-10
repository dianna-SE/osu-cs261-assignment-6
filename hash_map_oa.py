# Name: Dianna Pham
# OSU Email:  phamdia@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 6 - HashMap (Portfolio Assignment): Open Addressing
# Due Date: Aug 15, 2023
# Description: Implement methods within the HashMap class that integrates
#               proper open addressing techniques.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

        Table resizes are doubled from its capacity and the load factor is greater than or equal to 0.5.
        """
        new_entry = HashEntry(key, value)

        # resize if load factor greater than or equal to 0.5
        load_factor = self.table_load()

        if load_factor >= 0.5:
            double_capacity = self._capacity * 2
            self.resize_table(double_capacity)

        # get the hash value and its index
        hash_value = self._hash_function(key)
        initial_index = hash_value % self.get_capacity()
        index = initial_index

        j = 0
        while j < self._capacity:

            # insert key-value pairs at this index
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                self._buckets[index] = new_entry
                self._size += 1
                return

            # replace existing value with new value
            elif self._buckets[index].key == key:
                self._buckets[index].value = value
                return

            # traverse to the next index using quadratic probing
            j += 1
            index = (initial_index + j ** 2) % self._capacity

    def table_load(self) -> float:
        """
        Method that returns the load factor of the hash table.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method that simply returns how many empty buckets exist within the hash table.
        """
        # m total slots and n filled slots, so m − n open spots.
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Method that changes the capacity of the hash table and rehashes existing key-value pairs into
        the new hash map.
        """
        # print("resizing! load factor: ", self.table_load())
        if new_capacity < self._size:
            return

        # check prime and get the next prime if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create new hash map to rehash innards
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # rehash key-value pairs
        for num in range(self._capacity):
            item = self._buckets[num]

            if item and not item.is_tombstone:
                new_hash_map.put(item.key, item.value)

        # update new values of new hash map
        self._buckets, self._capacity = new_hash_map._buckets, new_hash_map._capacity
        self._size = new_hash_map._size

    def get(self, key: str) -> object:
        """
        Method that returns the value using the key and returns None if the key does not exist within
        the hash map.
        """
        hash_value = self._hash_function(key)
        initial_index = hash_value % self.get_capacity()
        index = initial_index

        # quadratic probing loop
        j = 0
        while j < self._capacity:

            if self._buckets[index]:

                # check if the key was found
                if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                    return self._buckets[index].value

                # exit loop if tombstone encountered
                # elif self._buckets[index].is_tombstone:
                #     pass

            # compute the next index in the probing sequence and repeat
            j += 1
            index = (initial_index + j ** 2) % self._capacity

        return None

    def contains_key(self, key: str) -> bool:
        """
        Method that returns True if there exists the key in the hash map and returns False if it does not
        (i.e., empty hash map).
        """
        # empty hash map, return false
        if self._size == 0:
            return False

        # get value at this index using the key
        hash_value = self._hash_function(key)
        initial_index = hash_value % self.get_capacity()
        index = initial_index

        # quadratic probing loop
        j = 0
        while j < self._capacity:

            # key is present
            if self._buckets[index] and self._buckets[index].key == key:
                return True

            # compute the next index in the probing sequence
            j += 1
            index = (initial_index + j ** 2) % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        Method that simply removes the given key-value pair from the hash map.
        """
        hash_value = self._hash_function(key)
        initial_index = hash_value % self.get_capacity()
        index = initial_index

        # quadratic probing loop
        j = 0
        while j < self._capacity:

            if self._buckets[index]:

                # key found, replace with tombstone and decrement size
                if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return

            # compute the next index in the probing sequence and repeat
            j += 1
            index = (initial_index + j ** 2) % self._capacity

    def clear(self) -> None:
        """
        Method that wipes out the contents in the hash map without changing the capacity.
        """
        # reset with a blank dynamic array
        self._buckets = DynamicArray()

        # append any slots in array as none and reset size
        for num in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method that returns a dynamic array of indexes of tuple key-value pairs within the hash map
        in any key order.
        """
        keys_and_values = DynamicArray()

        # append any key-value pairs that are not tombstones into hash map
        hash_map = self

        for num in hash_map:
            if num is not None and num.is_tombstone is False:
                keys_and_values.append((num.key, num.value))

        return keys_and_values

    def __iter__(self):
        """
        Method that allows hash map iteration on itself.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Method that returns the next item in the hash map according to where the iterator location is.
        """
        # raise exception error that terminates loop (exceeds array boundary)
        if self._index >= self._buckets.length():
            raise StopIteration

        # retrieves value at current index
        item = self._buckets.get_at_index(self._index)
        self._index += 1

        # traverse past empty buckets and tombstones
        while item is None or item.is_tombstone:

            # ends loop if exceeds array boundary
            if self._index >= self._buckets.length():
                raise StopIteration

            # get value at current index and traverse to the next one
            item = self._buckets.get_at_index(self._index)
            self._index += 1

        return item


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    # #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
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
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
