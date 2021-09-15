import random
from datetime import datetime


def get_password(password_length=6, by_chance=None) -> str:
    """
    Сгенерировать пароль пользователя по умолчанию.
    Если by_chance=True, то пароль - набор случайных символов, длинной password_length.
    Если by_chance=None, то пароль - текщий месяц, плюс год со строчной буквы, например, май2021.
    :return: Пароль пользователя
    """
    if by_chance:
        numbers = "1234567890"
        letters_lower = "abcdefghijklmnopqrstuvwxyz"
        letters_upper = letters_lower.upper()
        sequence = list(numbers + letters_lower + letters_upper)
        # Перемешать список
        random.shuffle(sequence)
        return "".join([random.choice(sequence) for _ in range(password_length)])
    else:
        list_of_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
        date = datetime.now()
        month = date.month
        year = date.year
        return list_of_months[month - 1] + str(year)
