# Homework on "Algorithms for Big Data Processing"

Welcome! How are you feeling? We hope you're excited for a new challenge! 😉
Today, you'll gain hands-on experience with Bloom filters and the HyperLogLog algorithm to solve real-world problems.

This homework consists of two independent tasks.

- Task 1 (Checking password uniqueness) will introduce you to designing systems that handle large-scale data efficiently, minimizing memory usage while maintaining high processing speed.

- Task 2 (Unique element counting) will teach you to compare exact counting methods against approximate algorithms like HyperLogLog, evaluating their performance and execution time.

Let’s get started! 💪🏼

## [Solutions](./solution.md)

---

## Task 1: Checking Password Uniqueness with a Bloom Filter

Implement a function to check password uniqueness using a Bloom filter. This function should determine whether a password has been used before without storing the passwords themselves.

### Technical Requirements

1. Implement a `BloomFilter` class that supports adding elements and checking membership.
2. Implement `check_password_uniqueness`, which utilizes a `BloomFilter` instance to check a list of new passwords for uniqueness.
3. Ensure robust data handling: passwords should be treated as plain strings (no hashing). Handle empty or invalid inputs appropriately.
4. The solution must work with large datasets while using minimal memory.

### Acceptance Criteria

📌 If any criterion is not met, the task will be sent back for revision.

1. `BloomFilter` correctly implements the Bloom filter logic (20 points).
2. `check_password_uniqueness` accurately determines password uniqueness (20 points).
3. The code produces the expected output (10 points).

### Example Usage

```python
if __name__ == "__main__":
    # Initialize Bloom Filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Check new passwords
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print results
    for password, status in results.items():
        print(f"Password '{password}' - {status}.")

```

### Expected Output

```python
Password 'password123' - already used.
Password 'newpassword' - unique.
Password 'admin123' - already used.
Password 'guest' - unique.
```

---

## Task 2: Comparing HyperLogLog Performance vs. Exact Counting

Develop a script to compare exact counting and HyperLogLog-based counting of unique elements.

### Technical Requirements

1. Load real-world data from `lms-stage-access.log`, which contains IP address information.
2. Implement an exact unique IP count using a `set`.
3. Implement an approximate unique IP count using HyperLogLog.
4. Compare both methods based on execution time.

### Acceptance Criteria

1. The data loading function correctly processes the log file, ignoring invalid lines (10 points).
2. The exact counting function correctly counts unique IPs (10 points).
3. HyperLogLog provides results within acceptable error margins (10 points).
4. The results comparison is displayed in a table format (10 points).
5. The implementation is optimized for large datasets (10 points).

### Example Output

```python
Comparison Results:
                       Exact Counting   HyperLogLog
Unique Elements              100000.0      99652.0
Execution Time (sec)             0.45          0.1
```
