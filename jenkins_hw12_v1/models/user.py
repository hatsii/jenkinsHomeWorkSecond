from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List


class Gender(str, Enum):
    male = 'Male'
    female = 'Female'
    other = 'Other'


class Hobby(str, Enum):
    sports = 'Sports'
    reading = 'Reading'
    music = 'Music'


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gender: Gender
    phone: str
    birth_date: date
    subjects: List[str] = field(default_factory=list)
    hobbies: List[Hobby] = field(default_factory=list)
    picture: str = ''           # имя файла в /resources (например, 'cat.png')
    address: str = ''
    state: str = ''
    city: str = ''

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def dob_for_result(self) -> str:
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        return f'{self.birth_date.day} {months[self.birth_date.month - 1]},{self.birth_date.year}'
