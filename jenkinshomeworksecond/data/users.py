from datetime import date
from jenkinshomeworksecond.models.user import User, Gender, Hobby

# Пользователь для тестов
student = User(
    first_name='Vadim',
    last_name='Tatarnikov',
    email='examplemail213@mail.ru',
    gender=Gender.male,
    phone='4564978762',
    birth_date=date(2003, 4, 23),
    subjects=['Chemistry'],
    hobbies=[Hobby.reading],
    picture='exampleImage.png',
    address='fgfggfgf,Test str., 1',
    state='Haryana',
    city='Karnal',
)
