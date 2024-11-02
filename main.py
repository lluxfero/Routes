from module_simulation import generate_atms, simulate_service_needs  # импортируем функции для генерации банкоматов и симуляции
from module_routes import plan_routes  # импортируем функцию для планирования маршрутов

import matplotlib.pyplot as plt

def plot_routes(planned_routes):
    for day, route_info in planned_routes.items():
        plt.figure(figsize=(10, 6))
        plt.title(f'Маршруты на день {day + 1}')
        plt.xlabel('Координата X')
        plt.ylabel('Координата Y')

        for group_id, route in route_info['routes'].items():
            x_coords = [atm.x for atm in route]
            y_coords = [atm.y for atm in route]
            x_coords.insert(0, 5)
            x_coords.append(5)
            y_coords.insert(0, 5)
            y_coords.append(5)
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', label=f'Группа {group_id + 1}')

        if route_info['unassigned']:
            unassigned_x = [atm.x for atm in route_info['unassigned']]
            unassigned_y = [atm.y for atm in route_info['unassigned']]
            plt.scatter(unassigned_x, unassigned_y, c='red', marker='x', label='Не назначенные банкоматы')

        plt.legend()
        plt.grid(True)
        plt.show()

# вывод информации о маршрутах на каждый день
def log_routes(planned_routes, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for day, route_info in planned_routes.items():
            day_info = f"Маршруты на день {day + 1}:\n"  # выводим номер дня
            print(day_info)
            file.write(day_info)

            for group_id, route in route_info["routes"].items():
                group_info = f"  Группа {group_id + 1}:\n"  # выводим маршрут для каждой группы инкассаторов
                print(group_info)
                file.write(group_info)

                for atm in route:
                    atm_info = f"    - Банкомат ID: {atm.atm_id} (Координаты: {atm.x}, {atm.y})\n"  # выводим ID и координаты банкомата
                    print(atm_info)
                    file.write(atm_info)

            if route_info["unassigned"]:
                unassigned_info = "  Банкоматы, не назначенные на обслуживание:\n"  # выводим информацию о банкоматах, которые не удалось назначить на обслуживание
                print(unassigned_info)
                file.write(unassigned_info)

                for atm in route_info["unassigned"]:
                    unassigned_atm_info = f"    - Банкомат ID: {atm.atm_id} (Координаты: {atm.x}, {atm.y})\n"
                    print(unassigned_atm_info)
                    file.write(unassigned_atm_info)

            print()  # добавляем пустую строку для удобства чтения
            file.write('\n')  # добавляем пустую строку в файл для удобства чтения

# основные параметры
NUM_ATMS = 1000  # количество банкоматов
NUM_GROUPS = 5  # количество групп инкассаторов
WORKDAY_DURATION = 8 * 60  # продолжительность рабочего дня в минутах (8 часов)
SERVICE_TIME_PER_ATM = 10  # время обслуживания одного банкомата в минутах
AVERAGE_SPEED = 30  # средняя скорость движения инкассаторов в км/ч
NUM_DAYS = 7  # количество дней для симуляции маршрутов

# генерация банкоматов
atms = generate_atms(NUM_ATMS)  # генерируем список банкоматов с заданными характеристиками

# моделирование потребности в обслуживании на несколько дней вперед
atms_needing_service = simulate_service_needs(atms, NUM_DAYS)  # получаем банкоматы, нуждающиеся в обслуживании по дням

# планирование маршрутов для каждой группы инкассаторов на основе данных о банкоматах
planned_routes = plan_routes(
    atms_needing_service,  # данные о потребности в обслуживании
    NUM_GROUPS,  # количество групп инкассаторов
    WORKDAY_DURATION,  # продолжительность рабочего дня в минутах
    SERVICE_TIME_PER_ATM,  # время обслуживания одного банкомата
    AVERAGE_SPEED  # средняя скорость движения инкассаторов
)

log_routes(planned_routes, 'routes.txt')
plot_routes(planned_routes)