from createDB import Base


def get_base() -> Base:
    """
    Вспомогательная функция для alembic
    """
    from createDB import Library_Flask
    from createDB import User_Flask
    return Base
