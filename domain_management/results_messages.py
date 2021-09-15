import emoji


class ResultsMessages:
    """
    Класс сообщений о результатах выполнения команд
    """
    __EMOJI_CHECK_MARK = emoji.emojize(":check_mark:")
    __EMOJI_CROSS_MARK = emoji.emojize(":cross_mark:")

    USER_ACCOUNT_ADDED = f"{__EMOJI_CHECK_MARK} Учётная запись пользователя добавлена."
    ERROR_USER_ACCOUNT_ADDING = f"{__EMOJI_CROSS_MARK} Ошибка добавления учётной записи пользователя."

    USER_PASSWORD_SET = f"{__EMOJI_CHECK_MARK} Пароль учётной записи по умолчанию установлен."
    ERROR_USER_PASSWORD_SETTING = f"{__EMOJI_CROSS_MARK} Ошибка установки пароля учётной записи."

    USER_ACCOUNT_ATTRS_CHANGED = f"{__EMOJI_CHECK_MARK} Атрибуты учётной записи изменены."
    ERROR_USER_ACCOUNTS_ATTRS_CHANGING = f"{__EMOJI_CROSS_MARK} Ошибка изменения арибутов учётной записи."

    DIRECTORY_AND_PASSFILE_CREATED = f"{__EMOJI_CHECK_MARK} Директория пользователя и файл с паролем созданы."
    ERROR_CREATING_USER_DIRECTORY = f"{__EMOJI_CROSS_MARK} Ошибка создания директории пользователя или файла с паролем."

    PERMISSIONS_SET = f"{__EMOJI_CHECK_MARK} Права на директорию пользователя и на файл с паролем установлены."
    ERROR_SET_PERMISSION = f"{__EMOJI_CROSS_MARK} Ошибка установки прав директории пользователя."

    ERROR_CONNECTING_AD = f"{__EMOJI_CROSS_MARK} Ошибка подключения к серверу AD."
    ERROR_CONNECTING_SMB = f"{__EMOJI_CROSS_MARK} Ошибка подключения к SMB-серверу."

    CONNECTION_TO_AD_SUCCESSFUL = f"{__EMOJI_CHECK_MARK} Соединение с сервером AD успешно."
