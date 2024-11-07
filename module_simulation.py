from module_atm import ATM  # импортируем класс ATM из модуля module_atm
import random  # импортируем модуль random для генерации случайных значений

# - моделирует потребности банкоматов в обслуживании, 
# - генерирует список банкоматов с случайными параметрами,
# - управляет их состоянием на протяжении нескольких дней

# функция для генерации списка банкоматов с заданными параметрами
def generate_atms(num_atms):
    # создаем пустой список для банкоматов
    atms = []  
    for atm_id in range(num_atms):
        # задаем случайные параметры для бункеров и статистических характеристик банкомата
        receive_bin_capacity = random.randint(1000, 5000)  # емкость бункера приема
        dispense_bin_capacity = random.randint(1000, 5000) # емкость бункера выдачи
        receive_mean = random.uniform(100, 500)  # среднее количество поступлений
        receive_variance = random.uniform(10, 50)  # дисперсия поступлений
        dispense_mean = random.uniform(100, 500)  # среднее количество выдач
        dispense_variance = random.uniform(10, 50)  # дисперсия выдачи

        # создаем экземпляр класса ATM и добавляем его в список
        atm = ATM(
            atm_id=atm_id,
            receive_bin_capacity=receive_bin_capacity,
            dispense_bin_capacity=dispense_bin_capacity,
            receive_mean=receive_mean,
            receive_variance=receive_variance,
            dispense_mean=dispense_mean,
            dispense_variance=dispense_variance
        )
        
        # задаем случайные координаты банкомата в пределах 10 км x 10 км
        atm.x = random.uniform(0, 10)
        atm.y = random.uniform(0, 10)
        
        atms.append(atm)  # добавляем банкомат в список
    return atms  # возвращаем список банкоматов

# функция для моделирования потребности банкоматов в обслуживании на несколько дней вперед
def simulate_service_needs(atms, num_days):
    # создаем словарь для хранения банкоматов, нуждающихся в обслуживании каждый день
    atms_needing_service = {day: [] for day in range(num_days)}  

    for day in range(num_days):
        for atm in atms:
            if day == 0:
                # для первого дня определяем необходимость в обслуживании на основе текущих данных
                days_until_service = atm.days_until_service_needed()
                if days_until_service <= 1:
                    # добавляем банкомат, если он требует обслуживания
                    atms_needing_service[day].append(atm)  
            else:
                # обновляем уровни бункеров на следующий день
                atm.receive_bin_level += atm.receive_mean
                atm.dispense_bin_level -= atm.dispense_mean
                
                # корректируем уровни до максимально допустимых значений
                atm.receive_bin_level = min(atm.receive_bin_level, atm.receive_bin_capacity)
                atm.dispense_bin_level = max(atm.dispense_bin_level, 0)
                
                # проверяем необходимость в обслуживании
                if atm.receive_bin_level >= atm.receive_bin_capacity or atm.dispense_bin_level <= 0:
                    atms_needing_service[day].append(atm)  # добавляем банкомат в список на обслуживание
                    # сбрасываем уровни бункеров после обслуживания
                    atm.receive_bin_level = atm.receive_bin_capacity / 2
                    atm.dispense_bin_level = atm.dispense_bin_capacity / 2
    # возвращаем словарь с банкоматами, нуждающимися в обслуживании
    return atms_needing_service  
