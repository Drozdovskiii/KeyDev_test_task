import os
import re
from collections import defaultdict

def analyze_log(log_file):
    # Путь к файлу
    file_path = os.path.abspath(log_file)

    # Инициализация переменных
    total_lines = 0
    local_requests = 0
    private_network_requests = 0
    external_network_requests = 0
    successful_requests = 0
    unsuccessful_requests = 0
    ip_counts = defaultdict(int)

    # Маски для IP адресов
    local_ip = "127.0.0.1"
    private_ip_ranges = [
        "10.",        # 10.0.0.0/8
        "172.",       # 172.16.0.0/12
        "192.168."    # 192.168.0.0/16
    ]

    # Открываем лог-файл для анализа
    with open(log_file, 'r') as f:
        for line in f:
            total_lines += 1
            # Регулярное выражение для извлечения IP и кода ответа
            match = re.match(r'(\S+) - - \[\S+ \+\d+\] "(\S+) \S+ \S+" (\d{3}) \S+', line)
            if match:
                ip = match.group(1)
                status_code = match.group(3)
                ip_counts[ip] += 1

                # Подсчитываем запросы в зависимости от типа сети
                if ip == local_ip:
                    local_requests += 1
                elif any(ip.startswith(prefix) for prefix in private_ip_ranges):
                    private_network_requests += 1
                else:
                    external_network_requests += 1

                # Подсчитываем успешные и неуспешные запросы
                if status_code.startswith('2') or status_code.startswith('3'):
                    successful_requests += 1
                else:
                    unsuccessful_requests += 1

    # Вывод информации
    print(f"Общее количество строк в файле: {total_lines}")
    print(f"Физический путь к файлу: {file_path}")
    print(f"Количество запросов с локального адреса: {local_requests}")
    print(f"Количество запросов с непубличной сети: {private_network_requests}")
    print(f"Количество запросов с внешней сети: {external_network_requests}")
    print(f"Количество успешных запросов: {successful_requests}")
    print(f"Количество неуспешных запросов: {unsuccessful_requests}")
    print("Список уникальных IP и количество запросов с них:")
    
    for ip, count in ip_counts.items():
        print(f"IP: {ip}, Количество запросов: {count}")

if __name__ == '__main__':
    # Путь к лог файлам в каталоге ./logs
    log_directory = './logs'  # Путь к логам изменен на относительный

    # Проверяем, существует ли директория logs
    if not os.path.exists(log_directory):
        print(f"Ошибка: Директория {log_directory} не существует!")
    else:
        # Ищем все лог файлы в каталоге ./logs
        for filename in os.listdir(log_directory):
            if filename.endswith('.log'):
                log_file = os.path.join(log_directory, filename)
                print(f"\nАнализируем файл: {log_file}")
                analyze_log(log_file)
