from dataclasses import dataclass
from typing import List, Dict


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
    """Тренировка: бег."""
    CFCL_RUN_MLTPLC: int = 18
    CFCL_RUN_SBTRC: int = 20
    CNST_MINHR_RUN: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.CFCL_RUN_MLTPLC * self.get_mean_speed()
             - self.CFCL_RUN_SBTRC)
            * self.weight / self.M_IN_KM * self.duration * self.CNST_MINHR_RUN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CFCL_WLK_MLTPLC1: float = 0.035
    CFCL_WLK_XPNTN: int = 2
    CFCL_WLK_MLTPLC2: float = 0.029
    CNST_MINHR_WLK: int = 60

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
        return (
            (self.CFCL_WLK_MLTPLC1 * self.weight
             + (self.get_mean_speed()**self.CFCL_WLK_XPNTN // self.height)
             * self.CFCL_WLK_MLTPLC2 * self.weight)
            * self.duration * self.CNST_MINHR_WLK)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CFCL_SWM_MLTPLC: int = 2
    CFCL_SWM_DDTN: float = 1.1

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
        return (
            (self.get_mean_speed() + self.CFCL_SWM_DDTN)
            * self.CFCL_SWM_MLTPLC * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_class: Dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout_type_class:
        raise KeyError(f'Неизвестный идентификатор спорта: {workout_type}')

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
        training = read_package(workout_type, data)
        main(training)
