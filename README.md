# HashMap - Portfolio Assignment

Data Structure & Algorithms
Implemented a codebase that handled collisions through open addressing and separate chaining while maintaining an efficient runtime complexity of O(1). There are two files -- one that implements a HashMap using separate chaining with linked lists, and the other implements HashMap with quadratic probing.

A hash function is used to convert each key into an index in an array where the corresponding value can be stored. Collisions can occur where two different keys could hash to the same index. In order to prevent collisions, there are two methods, separate chaining and quadratic probing.

## Separate Chaining
One strategy for dealing with collisions is called "separate chaining." When a collision occurs where two keys are hashed to the same index, the values are simply added into a "collection", or a linked list at that index. Here, we call them "buckets". 

## Quadratic Probing
The second strategy for dealing with collisions is called "quadratic probing." Instead of using buckets, the map is simply 'probed' by a computation to find the next available index. The key value pair is then stored once an empty slot is found. The computation for quadratic probing is (index + i ** 2) % size.

## Instructions
- To run the program, download the files and open the files using the IDE of preference.
- Run the code through your IDE.
