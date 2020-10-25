import csv
from distutils.util import strtobool

from lib.recipe import Recipe

def get_recipe_for_item(recipe_list, item):
    """
    Not all items are recipes, but if an item is a recipe we want to know more about it
    """
    for recipe in recipe_list:
        if item == recipe.item_result:
            return recipe
    return None

def parse_indices_from_header_row(row):
    key = row.index("#")
    number = row.index("Number")
    craft_type = row.index("CraftType")
    recipe_level_table = row.index("RecipeLevelTable")
    item_result = row.index(r"Item{Result}")
    amount_result = row.index(r"Amount{Result}")

    start_item_ingredients = row.index(r"Item{Ingredient}[0]")
    end_item_ingredients = row.index(r"Amount{Ingredient}[9]")

    is_secondary = row.index("IsSecondary")
    material_quality_factor = row.index("MaterialQualityFactor")
    difficulty_factor = row.index("DifficultyFactor")
    quality_factor = row.index("QualityFactor")
    durability_factor = row.index("DurabilityFactor")
    required_craftsmanship = row.index("RequiredCraftsmanship")
    required_control = row.index("RequiredControl")
    quick_synth_craftsmanship = row.index("QuickSynthCraftsmanship")
    quick_synth_control = row.index("QuickSynthControl")
    secret_recipe_book = row.index("SecretRecipeBook")
    can_quick_synth = row.index("CanQuickSynth")
    can_hq = row.index("CanHq")
    exp_rewarded = row.index("ExpRewarded")
    status_required = row.index(r"Status{Required}")
    item_required = row.index(r"Item{Required}")
    is_specialization_required = row.index("IsSpecializationRequired")
    is_expert = row.index("IsExpert")
    patch_number = row.index("PatchNumber")

    indices = {
        "key": key,
        "number": number,
        "craft_type": craft_type,
        "recipe_level_table": recipe_level_table,
        "item_result": item_result,
        "amount_result": amount_result,
        "start_item_ingredients": start_item_ingredients,
        "end_item_ingredients": end_item_ingredients,
        "is_secondary": is_secondary,
        "material_quality_factor": material_quality_factor,
        "difficulty_factor": difficulty_factor,
        "quality_factor": quality_factor,
        "durability_factor": durability_factor,
        "required_craftsmanship": required_craftsmanship,
        "required_control": required_control,
        "quick_synth_craftsmanship": quick_synth_craftsmanship,
        "quick_synth_control": quick_synth_control,
        "secret_recipe_book": secret_recipe_book,
        "can_quick_synth": can_quick_synth,
        "can_hq": can_hq,
        "exp_rewarded": exp_rewarded,
        "status_required": status_required,
        "item_required": item_required,
        "is_specialization_required": is_specialization_required,
        "is_expert": is_expert,
        "patch_number": patch_number,
    }

    return indices

def read_ingredient_list(row, start, end):
    possible_ingredient_set = row[start:end+1]

    result = list(possible_ingredient_set[x: x + 2] for x in range(0, len(possible_ingredient_set), 2))
    return_list = []
    for pair in result:
        if pair[0] != '':
            return_list.append(pair)
    return return_list

def read_recipe_csv(path, version):
    csv_path = F"{path}\\{version}\\exd\\Recipe.csv"
    recipe_list = []
    with open(csv_path, 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        _index_row = next(reader)
        header_row = next(reader)
        header_indices = parse_indices_from_header_row(header_row)
        _data_type_row = next(reader)
        for row in reader:
            recipe = Recipe()
            recipe.key = row[header_indices["key"]]
            recipe.number = row[header_indices["number"]]
            recipe.craft_type = row[header_indices["craft_type"]]
            recipe.recipe_level_table = row[header_indices["recipe_level_table"]]
            recipe.item_result = row[header_indices["item_result"]]
            recipe.amount_result = row[header_indices["amount_result"]]
            recipe.is_secondary = strtobool(row[header_indices["is_secondary"]])
            recipe.material_quality_factor = row[header_indices["material_quality_factor"]]
            recipe.difficulty_factor = row[header_indices["difficulty_factor"]]
            recipe.quality_factor = row[header_indices["quality_factor"]]
            recipe.durability_factor = row[header_indices["durability_factor"]]
            recipe.required_craftsmanship = row[header_indices["required_craftsmanship"]]
            recipe.required_control = row[header_indices["required_control"]]
            recipe.quick_synth_craftsmanship = row[header_indices["quick_synth_craftsmanship"]]
            recipe.quick_synth_control = row[header_indices["quick_synth_control"]]
            recipe.secret_recipe_book = row[header_indices["secret_recipe_book"]]
            recipe.can_quick_synth = strtobool(row[header_indices["can_quick_synth"]])
            recipe.can_hq = strtobool(row[header_indices["can_hq"]])
            recipe.exp_rewarded = strtobool(row[header_indices["exp_rewarded"]])
            recipe.status_required = row[header_indices["status_required"]]
            recipe.item_required = row[header_indices["item_required"]]
            recipe.is_specialization_required = strtobool(row[header_indices["is_specialization_required"]])
            recipe.is_expert = strtobool(row[header_indices["is_expert"]])
            recipe.patch_number = int(row[header_indices["patch_number"]])

            recipe.ingredients = read_ingredient_list(row, header_indices["start_item_ingredients"], header_indices["end_item_ingredients"])
            recipe.num_ingredients = len(recipe.ingredients)
            recipe_list.append(recipe)

    return recipe_list

