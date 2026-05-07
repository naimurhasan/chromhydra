from chromhydra.hints.grease import greased_brand

ORDERS = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))


def brand_list(full_version: str, product: str = "Google Chrome") -> list[dict]:
    major = int(full_version.split(".")[0])
    grease, grease_version = greased_brand(major)
    base = (
        {"brand": grease, "version": grease_version, "full_version": f"{grease_version}.0.0.0"},
        {"brand": "Chromium", "version": str(major), "full_version": full_version},
        {"brand": product, "version": str(major), "full_version": full_version},
    )
    shuffled = [{}] * len(base)
    for index, position in enumerate(ORDERS[major % len(ORDERS)]):
        shuffled[position] = base[index]
    return shuffled
