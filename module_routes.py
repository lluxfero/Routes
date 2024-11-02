from module_simulation import simulate_service_needs  # импортируем функцию для симуляции
import random  # импортируем модуль random для случайного распределения
import math  # импортируем модуль math для вычисления расстояний

# функция для планирования маршрутов на основе списка банкоматов, нуждающихся в обслуживании
def plan_routes(atms_needing_service, num_groups, workday_duration, service_time_per_atm, average_speed):
    planned_routes = {}  # создаем словарь для хранения маршрутов по дням

    # функция для определения к какой группе относится банкомат, основываясь на его координатах
    def determine_group(atm):
        return atm.x // (10 / num_groups)  # делим город на части по x-координате

    # функция для вычисления расстояния между двумя банкоматами
    def distance(atm1, atm2):
        return math.sqrt((atm1.x - atm2.x) ** 2 + (atm1.y - atm2.y) ** 2)  # вычисляем расстояние по теореме Пифагора

    for day, atms_today in atms_needing_service.items():
        group_routes = {group_id: [] for group_id in range(num_groups)}  # инициализируем группы для маршрутов
        group_times = {group_id: 0 for group_id in range(num_groups)}  # инициализируем время для каждой группы
        unassigned_atms = []  # список для банкоматов, которые не удалось назначить
        visited_atms = set()  # множество для отслеживания посещенных банкоматов

        for atm in atms_today:
            group_id = determine_group(atm)  # определяем, к какой группе относится банкомат
            if group_id >= num_groups:  # проверяем, корректен ли номер группы
                group_id = num_groups - 1  # назначаем последней группе, если номер превышает количество групп
            
            if not group_routes[group_id]:  # проверяем, есть ли уже маршруты для данной группы
                group_routes[group_id].append(atm)  # добавляем банкомат в маршрут группы
                group_times[group_id] = service_time_per_atm  # устанавливаем начальное время обслуживания
                visited_atms.add(atm)  # добавляем банкомат в посещенные
            else:
                last_atm = group_routes[group_id][-1]  # получаем последний банкомат в маршруте группы
                nearest_atm = None  # инициализируем ближайший банкомат
                min_distance = float('inf')  # устанавливаем минимальное расстояние на бесконечность
                
                for a in atms_today:
                    if a not in visited_atms:  # проверяем, был ли банкомат уже посещен
                        dist = distance(last_atm, a)  # вычисляем расстояние до банкомата
                        if dist < min_distance:  # если расстояние меньше текущего минимального
                            min_distance = dist  # обновляем минимальное расстояние
                            nearest_atm = a  # обновляем ближайший банкомат
                
                if nearest_atm:  # проверяем, найден ли ближайший банкомат
                    travel_time = (min_distance / average_speed) * 60  # вычисляем время пути в минутах
                    potential_total_time = group_times[group_id] + travel_time + service_time_per_atm  # вычисляем потенциальное общее время
                    
                    if potential_total_time <= workday_duration:  # проверяем, не превышает ли общее время рабочий день
                        group_routes[group_id].append(nearest_atm)  # добавляем ближайший банкомат в маршрут группы
                        group_times[group_id] = potential_total_time  # обновляем общее время группы
                        visited_atms.add(nearest_atm)  # добавляем банкомат в посещенные
                    else:
                        unassigned_atms.append(atm)  # добавляем банкомат в список не назначенных
        
        planned_routes[day] = {"routes": group_routes, "unassigned": unassigned_atms}  # сохраняем маршруты и информацию для каждого дня
    
    return planned_routes  # возвращаем маршруты по дням
