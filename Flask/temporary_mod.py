from createDB import Library_Flask, User_Flask, db_session
from faker import Faker
import random
faker_ = Faker('ru-RU')

for _ in range(10):
    new_user = User_Flask(
        name = faker_.first_name_female(),
        email= faker_.ascii_free_email(),
        password = 12345
    )

    db_session.add_all([new_user])
    db_session.commit()