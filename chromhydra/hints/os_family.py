FAMILIES = {"Android": "Linux", "Chrome OS": "Linux"}


def os_family(os_name: str) -> str:
    return FAMILIES.get(os_name, os_name)
