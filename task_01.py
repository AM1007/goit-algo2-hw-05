class BloomFilter:
    def __init__(self, size, num_hashes):
        """
        Ініціалізує фільтр Блума з заданим розміром та кількістю хеш-функцій
        
        Args:
            size (int): Розмір бітового масиву
            num_hashes (int): Кількість хеш-функцій
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size
    
    def _hash(self, item, seed):
        """
        Простий хеш-алгоритм для рядка з використанням seed для різних хеш-функцій
        
        Args:
            item (str): Елемент для хешування
            seed (int): Значення seed для створення унікальної хеш-функції
            
        Returns:
            int: Хеш-значення
        """
        result = 0
        for char in item:
            result = (result * seed + ord(char)) % self.size
        return result
    
    def add(self, item):
        """
        Додає елемент до фільтра Блума
        
        Args:
            item (str): Елемент для додавання
        """
        if not item or not isinstance(item, str):
            return
            
        for i in range(self.num_hashes):
            # Використовуємо різні seed для кожної хеш-функції
            hash_value = self._hash(item, i + 1)
            self.bit_array[hash_value] = 1
    
    def check(self, item):
        """
        Перевіряє, чи може елемент бути у фільтрі
        
        Args:
            item (str): Елемент для перевірки
            
        Returns:
            bool: True, якщо елемент можливо є у фільтрі, False - якщо точно відсутній
        """
        if not item or not isinstance(item, str):
            return False
            
        for i in range(self.num_hashes):
            hash_value = self._hash(item, i + 1)
            if self.bit_array[hash_value] == 0:
                return False
        return True

def check_password_uniqueness(bloom_filter, passwords):
    """
    Перевіряє унікальність паролів використовуючи фільтр Блума
    
    Args:
        bloom_filter (BloomFilter): Ініціалізований фільтр Блума з наявними паролями
        passwords (list): Список паролів для перевірки
        
    Returns:
        dict: Словник з результатами перевірки для кожного пароля
    """
    results = {}
    
    for password in passwords:
        if not password or not isinstance(password, str):
            results[password] = "некоректний пароль"
            continue
            
        if bloom_filter.check(password):
            results[password] = "вже використаний"
            # Не додаємо пароль, який потенційно вже існує
        else:
            results[password] = "унікальний"
            # Додаємо пароль до фільтра, оскільки він унікальний
            bloom_filter.add(password)
    
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)
    
    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)
        
    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)
    
    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")