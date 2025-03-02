import re
import time
import math
import mmh3

class HyperLogLog:
    def __init__(self, p=14):
        """
        Ініціалізує HyperLogLog з параметром точності p
        p = 14 дає похибку близько 1.6%
        
        Args:
            p (int): Параметр точності, що визначає кількість регістрів (2^p)
        """
        self.p = p
        self.m = 1 << p  # 2^p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha(self.m)
        
    def _get_alpha(self, m):
        """
        Повертає константу alpha для корекції оцінки
        """
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)
        
    def add(self, item):
        """
        Додає елемент до HyperLogLog
        
        Args:
            item (str): Елемент для додавання
        """
        # Використовуємо MurmurHash для хешування
        x = mmh3.hash(item, signed=False)
        
        # Знаходимо індекс регістра на основі перших p бітів
        j = x & (self.m - 1)
        
        # Кількість нулів перед першою 1 в інших бітах + 1
        w = x >> self.p
        leading_zeros = min(32, self._count_leading_zeros(w) + 1)
        
        # Оновлюємо регістр, якщо нове значення більше
        self.registers[j] = max(self.registers[j], leading_zeros)
    
    def _count_leading_zeros(self, value):
        """
        Підраховує кількість провідних нулів в бінарному представленні числа
        """
        if value == 0:
            return 32  # Для 32-бітних чисел
        
        count = 0
        while (value & 0x80000000) == 0:
            count += 1
            value <<= 1
        return count
    
    def count(self):
        """
        Оцінює кількість унікальних елементів
        
        Returns:
            float: Оцінка кількості унікальних елементів
        """
        # Обчислення гармонічного середнього
        sum_inv = 0
        for val in self.registers:
            sum_inv += 2 ** (-val)
        
        # Оцінка з корекцією
        raw_estimate = self.alpha * (self.m ** 2) / sum_inv
        
        # Корекції для малих та великих оцінок
        if raw_estimate <= 2.5 * self.m:
            # Корекція для малих оцінок
            # Підрахуємо кількість нульових регістрів
            zero_count = self.registers.count(0)
            if zero_count > 0:
                # Використовуємо лінійне підрахування для малих наборів
                return self.m * math.log(self.m / zero_count)
        
        return raw_estimate

def extract_ip_from_log(line):
    """
    Витягує IP-адресу з рядка логу
    
    Args:
        line (str): Рядок логу
        
    Returns:
        str: IP-адреса або None, якщо не знайдено
    """
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.match(ip_pattern, line)
    return match.group(0) if match else None

def load_data(file_path):
    """
    Завантажує IP-адреси з лог-файлу
    
    Args:
        file_path (str): Шлях до лог-файлу
        
    Returns:
        list: Список IP-адрес
    """
    ip_addresses = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                ip = extract_ip_from_log(line)
                if ip:
                    ip_addresses.append(ip)
    except Exception as e:
        print(f"Помилка при завантаженні файлу: {e}")
    
    return ip_addresses

def exact_count(ip_addresses):
    """
    Точний підрахунок унікальних IP-адрес
    
    Args:
        ip_addresses (list): Список IP-адрес
        
    Returns:
        int: Кількість унікальних IP-адрес
    """
    return len(set(ip_addresses))

def hll_count(ip_addresses, precision=14):
    """
    Підрахунок унікальних IP-адрес за допомогою HyperLogLog
    
    Args:
        ip_addresses (list): Список IP-адрес
        precision (int): Параметр точності для HyperLogLog
        
    Returns:
        float: Оцінка кількості унікальних IP-адрес
    """
    hll = HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    return hll.count()

def compare_methods(file_path):
    """
    Порівнює методи підрахунку унікальних IP-адрес
    
    Args:
        file_path (str): Шлях до лог-файлу
    """
    # Завантаження даних
    ip_addresses = load_data(file_path)
    
    # Точний підрахунок
    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time
    
    # HyperLogLog
    start_time = time.time()
    hll_result = hll_count(ip_addresses)
    hll_time = time.time() - start_time
    
    # Виведення результатів у форматі з прикладу
    print("Результати порівняння:")
    print(f"{'':25} {'Точний підрахунок':>20}   {'HyperLogLog':>10}")
    print(f"{'Унікальні елементи':25} {exact_result:>20.1f}   {hll_result:>10.1f}")
    print(f"{'Час виконання (сек.)':25} {exact_time:>20.2f}   {hll_time:>10.2f}")

if __name__ == "__main__":
    file_path = "lms-stage-access.log"
    compare_methods(file_path)