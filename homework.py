from dataclasses import dataclass
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
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
    LEN_STEP: float = 0.65  # константа для перевода движений в шаг, бег
    M_IN_KM: int = 1000  # константа для перевода м в км
    HOUR_TO_MIN: int = 60  # константа для перевода часов в минуты

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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Класс {self.__class__.__name__} должен '
                                  f'реализовывать метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    FIRST_RUN_RATIO: int = 18
    SECOND_RUN_RATIO: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.FIRST_RUN_RATIO
                 * self.get_mean_speed()
                 - self.SECOND_RUN_RATIO)
                * self.weight / self.M_IN_KM
                * (self.duration * self.HOUR_TO_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_WALK_RATIO: float = 0.035
    SECOND_WALK_RATIO: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.FIRST_WALK_RATIO * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.SECOND_WALK_RATIO * self.weight)
                * (self.duration * self.HOUR_TO_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # константа для перевода движений в пловки =)
    FIRST_SWIM_RATIO: float = 1.1
    SECOND_SWIM_RATIO: int = 2

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
                + self.FIRST_SWIM_RATIO)
                * self.SECOND_SWIM_RATIO
                * self.weight)


def read_package(workout: str, workout_data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport_type: Dict[str, Type[Training]] = {'SWM': Swimming, 'RUN': Running,
                                             'WLK': SportsWalking}
    if workout in sport_type:
        return sport_type[workout](*workout_data)
    raise ValueError


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
