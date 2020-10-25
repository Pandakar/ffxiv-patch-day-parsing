"""

"""

import csv
from distutils.util import strtobool
from lib.item import Item


def parse_boolean_string(input_string):
    """
    This exists because strtobool returns 0 or 1.
    I want true or false >=(.

    TODO add testing
    """
    return bool(strtobool(input_string))


def get_item_entry_for_item(item_list, item_name):
    for item in item_list:
        if item.name == item_name:
            return item

    return None


def parse_indices_from_header_row(row):
    key = row.index("#")
    description = row.index("Description")
    name = row.index("Name")
    icon = row.index("Icon")
    level_item = row.index(r"Level{Item}")
    rarity = row.index("Rarity")
    item_search_category = row.index("ItemSearchCategory")
    equip_slot_category = row.index("EquipSlotCategory")
    item_sort_category = row.index("ItemSortCategory")
    stack_size = row.index("StackSize")
    is_unique = row.index("IsUnique")
    is_untradable = row.index("IsUntradable")
    is_indisposable = row.index("IsIndisposable")
    can_be_hq = row.index("CanBeHq")
    is_collectable = row.index("IsCollectable")
    always_collectable = row.index("AlwaysCollectable")
    level_equip = row.index(r"Level{Equip}")
    equip_restriction = row.index("EquipRestriction")
    class_job_category = row.index("ClassJobCategory")

    indices = {
        "key": key,
        "description": description,
        "name": name,
        "icon": icon,
        "level_item": level_item,
        "rarity": rarity,
        "item_search_category": item_search_category,
        "equip_slot_category": equip_slot_category,
        "item_sort_category": item_sort_category,
        "stack_size": stack_size,
        "is_unique": is_unique,
        "is_untradable": is_untradable,
        "is_indisposable": is_indisposable,
        "can_be_hq": can_be_hq,
        "is_collectable": is_collectable,
        "always_collectable": always_collectable,
        "level_equip": level_equip,
        "equip_restriction": equip_restriction,
        "class_job_category": class_job_category,
    }
    return indices


def read_item_csv(path, version):
    csv_path = F"{path}\\{version}\\exd\\Item.csv"
    read_items = []
    with open(csv_path, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        _index_row = next(reader)
        header_row = next(reader)
        index = parse_indices_from_header_row(header_row)
        _data_type_row = next(reader)
        for row in reader:
            this_item = Item()
            this_item.key = int(row[index["key"]])
            this_item.name = row[index["name"]].strip()
            this_item.level_item = int(row[index["level_item"]])
            this_item.item_search_category = row[index["item_search_category"]].strip()
            this_item.stack_size = int(row[index["stack_size"]])
            this_item.is_unique = parse_boolean_string(row[index["is_unique"]])
            this_item.is_untradable = parse_boolean_string(row[index["is_untradable"]])
            this_item.is_indisposable = parse_boolean_string(row[index["is_indisposable"]])
            this_item.can_be_hq = parse_boolean_string(row[index["can_be_hq"]])
            this_item.is_collectable = parse_boolean_string(row[index["is_collectable"]])
            this_item.always_collectable = parse_boolean_string(row[index["always_collectable"]])
            this_item.level_equip = int(row[index["level_equip"]])
            this_item.equip_restriction = bool(row[index["equip_restriction"]])
            this_item.class_job_category = row[index["class_job_category"]]
            read_items.append(this_item)
    return read_items
