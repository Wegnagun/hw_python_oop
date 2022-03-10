from dataclasses import dataclass
from typing import List
import abc


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # переменная для перевода движений в шаг, бег
    M_IN_KM: int = 1000  # константа для перевода м в км
    HOUR_IN_MIN: int = 60  # константа для перевода часов в минуты

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
        return self.get_distance() / self.duration

    @abc.abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # TODO: переопределить в других классах

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    frst_run_multiplier: int = 18
    scnd_run_multiplier: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.frst_run_multiplier
                 * self.get_mean_speed()
                 - self.scnd_run_multiplier)
                * self.weight / self.M_IN_KM
                * (self.duration * self.HOUR_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    frst_wlk_multiplier: float = 0.035
    scnd_wlk_multiplier: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.frst_wlk_multiplier * self.
                weight + (self.get_mean_speed() ** 2 // self.
                          height) * self.scnd_wlk_multiplier * self.
                weight) * (self.duration * self.HOUR_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # константа для перевода движений в пловки =)
    frst_swm_multiplier: float = 1.1
    scnd_swm_multiplier: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.frst_swm_multiplier)
                * self.scnd_swm_multiplier
                * self.weight)


def read_package(workout: str, workout_data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    sport_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    try:
        return sport_type[workout](*workout_data)
    except LookupError:
        print(f"Исключение KeyError. Ключа '{workout}' нет в словаре.")


def main(train: Training) -> None:
    """Главная функция."""
    info = train.show_training_info()
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
