from domain_manager import DomainManager

dm = DomainManager("192.168.213.235", "CO\Administrator", "RP21-kmn10root")


if dm.is_connected:
    result = dm.add_user_account("Петушаркин Иван Сергеевич", "frontoffice", "+79994970133")
    print(result)
else:
    print("Что-то не то с подключением")

