from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: int
    duration: float
    distance: float
    speed: float
    calories: float

    """Вывести сообщение."""
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.action * self.LEN_STEP / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CFCL_RUN_1: int = 18
        CFCL_RUN_2: int = 20
        MINHR_RUN_3: int = 60
        return (
            (CFCL_RUN_1 * Training.get_mean_speed(self)
             - CFCL_RUN_2)
            * self.weight / self.M_IN_KM * self.duration * MINHR_RUN_3)


class SportsWalking(Training):
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CFCL_WLK_1: float = 0.035
        CFCL_WLK_2: int = 2
        CFCL_WLK_3: float = 0.029
        MINHR_WLK_4: int = 60
        return (
            (CFCL_WLK_1 * self.weight
             + (self.get_mean_speed()**CFCL_WLK_2 // self.height)
             * CFCL_WLK_3 * self.weight)
            * self.duration * MINHR_WLK_4)


class Swimming(Training):
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CFCL_SWM_1: int = 2
        CFCL_SWM_2: float = 1.1

        return (
            (self.get_mean_speed() + CFCL_SWM_2)
            * CFCL_SWM_1 * self.weight)


def read_package(workout_type: List[str], data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return workout_type_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        if (workout_type == 'SWM'
           or workout_type == 'RUN'
           or workout_type == 'WLK'):
            training = read_package(workout_type, data)
            main(training)
        else:
            print("Невозможно определить данные!")
