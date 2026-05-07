OPTION_NAMES = ("agent", "platform", "timezone", "locale", "proxy")


def chrome_options(headed: bool, **values) -> dict:
    options = {name: values.get(name) for name in OPTION_NAMES if values.get(name)}
    return {"headless": not headed, **options}
