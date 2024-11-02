from module_simulation import generate_atms, simulate_service_needs  # импортируем функции для генерации банкоматов и симуляции
from module_routes import plan_routes  # импортируем функцию для планирования маршрутов

import matplotlib.pyplot as plt

def plot_routes(atms, planned_routes):  # функция для построения маршрутов
    for day, route_info in planned_routes.items():  # итерируем по каждому дню и информации о маршруте
        plt.figure(figsize=(10, 6))  # создаем новую фигуру с размером 10x6
        plt.title(f'Маршруты на день {day + 1}')  # устанавливаем заголовок графика
        plt.xlabel('Координата X')  # устанавливаем метку для оси X
        plt.ylabel('Координата Y')  # устанавливаем метку для оси Y

        atms = [item for item in atms if item not in route_info['unassigned']]  # отфильтровываем обслуженные банкоматы
        successs_x = [atm.x for atm in atms]  # собираем X-координаты обслуженных банкоматов
        successs_y = [atm.y for atm in atms]  # собираем Y-координаты обслуженных банкоматов
        plt.scatter(successs_x, successs_y, c='green', marker='x', label='Все хорошо')  # наносим точки обслуженных банкоматов на график зеленым цветом

        for group_id, route in route_info['routes'].items():  # итерируем по каждой группе маршрутов
            x_coords = [atm.x for atm in route]  # собираем X-координаты банкоматов в маршруте
            y_coords = [atm.y for atm in route]  # собираем Y-координаты банкоматов в маршруте
            x_coords.insert(0, 5)  # добавляем начальную точку (базу) с координатой X
            x_coords.append(5)  # добавляем конечную точку (базу) с координатой X
            y_coords.insert(0, 5)  # добавляем начальную точку (базу) с координатой Y
            y_coords.append(5)  # добавляем конечную точку (базу) с координатой Y
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', label=f'Группа {group_id + 1}')  # наносим линии маршрутов на график

        if route_info['unassigned']:  # проверяем, есть ли не назначенные банкоматы
            unassigned_x = [atm.x for atm in route_info['unassigned']]  # собираем X-координаты не назначенных банкоматов
            unassigned_y = [atm.y for atm in route_info['unassigned']]  # собираем Y-координаты не назначенных банкоматов
            plt.scatter(unassigned_x, unassigned_y, c='red', marker='x', label='Не назначенные банкоматы')  # наносим точки не назначенных банкоматов на график красным цветом

        plt.legend()  # добавляем легенду к графику
        plt.grid(True)  # добавляем сетку к графику
        plt.show()  # отображаем график

# вывод информации о маршрутах на каждый день
def log_routes(planned_routes, filename):  # функция для логирования маршрутов в файл
    with open(filename, 'w', encoding='utf-8') as file:  # открываем файл для записи
        for day, route_info in planned_routes.items():  # итерируем по каждому дню и информации о маршруте
            day_info = f"Маршруты на день {day + 1}:\n"  # выводим номер дня
            print(day_info)  # печатаем информацию о дне на экран
            file.write(day_info)  # записываем информацию о дне в файл

            for group_id, route in route_info["routes"].items():  # итерируем по каждой группе маршрутов
                group_info = f"  Группа {group_id + 1}:\n"  # выводим маршрут для каждой группы инкассаторов
                print(group_info)  # печатаем информацию о группе на экран
                file.write(group_info)  # записываем информацию о группе в файл

                for atm in route:  # итерируем по каждому банкомату в маршруте
                    atm_info = f"    - Банкомат ID: {atm.atm_id} (Координаты: {atm.x}, {atm.y})\n"  # выводим ID и координаты банкомата
                    print(atm_info)  # печатаем информацию о банкомате на экран
                    file.write(atm_info)  # записываем информацию о банкомате в файл

            if route_info["unassigned"]:  # проверяем, есть ли не назначенные банкоматы
                unassigned_info = "  Банкоматы, не назначенные на обслуживание:\n"  # выводим информацию о банкоматах, которые не удалось назначить на обслуживание
                print(unassigned_info)  # печатаем информацию о не назначенных банкоматах на экран
                file.write(unassigned_info)  # записываем информацию о не назначенных банкоматах в файл

                for atm in route_info["unassigned"]:  # итерируем по каждому не назначенному банкомату
                    unassigned_atm_info = f"    - Банкомат ID: {atm.atm_id} (Координаты: {atm.x}, {atm.y})\n"  # выводим ID и координаты банкомата
                    print(unassigned_atm_info)  # печатаем информацию о не назначенном банкомате на экран
                    file.write(unassigned_atm_info)  # записываем информацию о не назначенном банкомате в файл

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
plot_routes(atms, planned_routes)