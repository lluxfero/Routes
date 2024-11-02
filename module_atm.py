import random  # импортируем модуль random для генерации случайных значений

class ATM:
    # инициализируем класс ATM, задаем характеристики банкомата
    def __init__(self, atm_id, receive_bin_capacity, dispense_bin_capacity,
                 receive_mean, receive_variance,
                 dispense_mean, dispense_variance):
        self.atm_id = atm_id  # уникальный идентификатор банкомата
        self.receive_bin_capacity = receive_bin_capacity  # емкость бункера для приема
        self.dispense_bin_capacity = dispense_bin_capacity  # емкость бункера для выдачи
        self.receive_bin_level = receive_bin_capacity / 2  # начальное заполнение бункера приема
        self.dispense_bin_level = dispense_bin_capacity / 2  # начальное заполнение бункера выдачи
        self.receive_mean = receive_mean  # математическое ожидание поступлений
        self.receive_variance = receive_variance  # дисперсия поступлений
        self.dispense_mean = dispense_mean  # математическое ожидание выдачи
        self.dispense_variance = dispense_variance  # дисперсия выдачи

    # метод для расчета количества дней до переполнения/опустошения бункера
    def days_until_service_needed(self):
        # вычисляем дни до переполнения бункера приема
        if self.receive_mean > 0:
            days_to_overflow = (self.receive_bin_capacity - self.receive_bin_level) / self.receive_mean
        else:
            days_to_overflow = float('inf')  # бесконечность, если нет поступлений
        
        # вычисляем дни до опустошения бункера выдачи
        if self.dispense_mean > 0:
            days_to_empty = self.dispense_bin_level / self.dispense_mean
        else:
            days_to_empty = float('inf')  # бесконечность, если нет выдачи
        
        # выбираем минимум из этих значений
        days_until_service = min(days_to_overflow, days_to_empty)
        return days_until_service  # возвращаем минимальное количество дней до обслуживания