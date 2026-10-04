import json


def load_map(file_name: str = "level_data.json") -> dict[int, dict]:
    clear_map: dict[int, dict] = {}

    try:
        with open(file_name, "r") as file:
            level_map = json.load(file)
    except FileNotFoundError:
        clear_map = {
            1: {
                "floor": [
                    [0, 320],
                    [64, 320],
                    [128, 320],
                    [192, 320],
                    [256, 320],
                    [320, 320],
                    [384, 320],
                    [448, 320],
                ],
                "lava": [[256, 320]],
            }
        }
    else:
        for key, value in level_map.items():
            clear_map[int(key)] = value

    return clear_map


def import_map(platform: list, level: int, file_name: str = "level_data.json") -> None:
    """Сохраняет отредактированную карту под номер level"""
    level_map: dict[int, dict] = load_map()
    level_map[level] = {"floor": [], "lava": []}

    for block in platform:
        if block.type_block == "floor":
            level_map[level]["floor"].append(block.rect.topleft)
        elif block.type_block == "lava":
            level_map[level]["lava"].append(block.rect.topleft)

    with open(file_name, "w") as file:
        json.dump(level_map, file)
