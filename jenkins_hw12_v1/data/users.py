from datetime import date
from jenkins_hw12_v1.models.user import User, Gender, Hobby

# Пользователь для тестов
student = User(
    first_name='Liza',
    last_name='Koss',
    email='lizakoss@mailinator.com',
    gender=Gender.female,
    phone='4564978762',
    birth_date=date(2000, 3, 15),
    subjects=['Chemistry'],
    hobbies=[Hobby.reading],
    picture='cat.png',
    address='Sevastopol,Test str., 1',
    state='Haryana',
    city='Karnal',
)
