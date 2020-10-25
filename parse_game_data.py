"""
Module designed to parse and interpret exd files from Final Fantasy XIV.
The info I cared about parsing here was for items and recipes, largely
for day 1 crafting ahead of main sites updating.
"""
import argparse
import csv
import os
import subprocess
import sys
import yaml

from lib.item import Item
import google_sheets_connector
import import_item
import import_recipe

LAST_RAID_PATCH = 520
CURRENT_MAIN_PATCH = 535
EXPECTED_GEAR_ILV = "480"


def get_current_game_version(ffxiv_install_location):
    """
    Find the current version of your locally installed FFXIV copy.

    This is important for actually finding the dumped files.
    Files get stored under {SaintCoinach.Cmd.exe}/{version}/exd/.
    """
    ffxiv_file = F"{ffxiv_install_location}\\game\\ffxivgame.ver"
    with open(ffxiv_file, "r") as version_file:
        return version_file.readline()


def run_exporter(ffxiv_install_location, saint_coinach_install_location):
    """
    Run the data mining tool.
    Requires changing directory to use all of the associated DLLs.
    After we finish, switch back to our directory for continued processing.

    Unfortunately running the data mining tool like this forces us
    to dump all tables, you can't input something like:
    `SaintCoinach.Cmd.exe Item Recipe`
    and get only those two tables.
    You would have to enter the tool's CLI to do that.
    """
    script_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(saint_coinach_install_location)
    result = subprocess.getoutput([".\\SaintCoinach.Cmd.exe",
                                   F"{ffxiv_install_location}",
                                   "exd"])

    os.chdir(script_path)
    print(F"Done processing! {result}")


def create_local_csvs(game_version, item_list, recipe_list):
    output_path = F"./debug_csvs/{game_version}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    header_row = Item().__dict__.keys()
    item_file = F"{output_path}/filtered_items.csv"
    ingredients_file = F"{output_path}/filtered_recipe_ingredients.csv"
    recipe_meta_file = F"{output_path}/recipe_meta_information.csv"
    with open(item_file, "w", newline='', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header_row)
        writer.writeheader()
        writer.writerows([item.__dict__ for item in item_list])

    data = []
    header = ["recipe_name", "material", "amount"]
    for recipe in recipe_list:
        for ingredient, amount in recipe.ingredients:
            row = {"recipe_name": recipe.item_result.strip(), "material": ingredient.strip(), "amount": amount.strip()}
            data.append(row)

    with open(ingredients_file, "w", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    data = []
    header = ["recipe_name",
              "craft_type",
              "yield_per_craft",
              "material_quality_factor",
              "difficulty_factor",
              "quality_factor",
              "durability_factor",
              "recipe_level_table_entry",
              "needs_specialist"]

    for recipe in recipe_list:
        row = {
            "recipe_name": recipe.item_result,
            "craft_type": recipe.craft_type,
            "yield_per_craft": recipe.amount_result,
            "material_quality_factor": recipe.material_quality_factor,
            "difficulty_factor": recipe.difficulty_factor,
            "quality_factor": recipe.quality_factor,
            "durability_factor": recipe.durability_factor,
            "recipe_level_table_entry": recipe.recipe_level_table,
            "needs_specialist": recipe.is_specialization_required
        }
        data.append(row)

    with open(recipe_meta_file, "w", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def verify_local_config():
    """
    Verify we have everything we need from the config file.
    If something's missing, tell user what config setting is missing before we blow remote stuff up.
    """
    config = yaml.safe_load(open("config.yml"))
    has_error = False

    if "ffxiv_install_location" not in config.keys():
        print("Need to define a line like the following in your local config.yml file: ")
        print("ffxiv_install_location: C:/Program Files (x86)/SquareEnix/FINAL FANTASY XIV - A Realm Reborn")
        print("This is needed to parse FFXIV's exd files.")
        has_error = True

    if "saint_coinach_install_location" not in config.keys():
        print("Need to define a line like the following in your local config.yml file:")
        print("saint_coinach_install_location: C:/Program Files/SaintCoinach.Cmd")
        print("Specifically, point this to the location where you have the SaintCoinach.Cmd.exe file.")
        print("If you do not have this, you can get it from: https://github.com/ufx/SaintCoinach/releases")
        has_error = True

    if "spreadsheet_id" not in config.keys():
        print("need spreadsheet id")
        has_error = True

    if "item_range" not in config.keys():
        print("need item range")
        has_error = True

    if "recipe_info_range" not in config.keys():
        print("need recipe_info_range defined")
        has_error = True

    if "recipe_materials_range" not in config.keys():
        print("need recipe_materials_range defined")
        has_error = True

    if has_error:
        print("")
        print("Address the above issues before rerunning.")
        sys.exit(0)

    return config

def get_all_required_recipes(recipes_to_process, filtered_item_list, recipe_list):
    """

    """
    processed_recipes = []
    # offload this into own procedure
    while len(recipes_to_process) > 0:
        recipe = recipes_to_process.pop()
        processed_recipes.append(recipe)
        ingredient_names = [x[0] for x in recipe.ingredients]
        for ingredient in ingredient_names:
            if ingredient not in filtered_item_list \
               and ingredient not in recipes_to_process:
                filtered_item_list.append(ingredient)
                new_recipe = import_recipe.get_recipe_for_item(recipe_list, ingredient)
                if new_recipe is not None:
                    recipes_to_process.append(new_recipe)

    return processed_recipes


def main():
    parser = argparse.ArgumentParser(description="Command-line tool to help parse exd files from FFXIV")
    parser.add_argument("--debug", dest="debug", action="store_true", help="Output additional local files for debug purposes.")
    parser.add_argument("--write-gsheet",  dest="write_gsheet", action="store_true", help="Write to an external Google Sheet (defined by local config.yml)")
    parser.add_argument("--skip-export", dest="skip_export", action="store_true", help="Skip running SaintCoinach exporter.")
    args = parser.parse_args()

    print("Reading config...")
    config = verify_local_config()
    ffxiv_install_location = config["ffxiv_install_location"]
    saint_coinach_install_location = config["saint_coinach_install_location"]

    print("Getting game version...")
    game_version = get_current_game_version(ffxiv_install_location)
    print(F"\tCurrent game version: {game_version}")
    if not args.skip_export:
        print("Running exporter...\n")
        run_exporter(ffxiv_install_location, saint_coinach_install_location)
        print("\nDone getting initial data dump! Reading relevant CSVs...")
    print("Reading item csv...")
    item_list = import_item.read_item_csv(saint_coinach_install_location, game_version)
    print("Reading recipe csv...")
    recipe_list = import_recipe.read_recipe_csv(saint_coinach_install_location, game_version)

    filtered_recipe_list = [x for x in recipe_list
                            if x.patch_number >= LAST_RAID_PATCH
                            and x.can_hq == 1
                            and EXPECTED_GEAR_ILV in x.recipe_level_table]
    filtered_item_list = [x.item_result for x in filtered_recipe_list]

    # Make a carbon copy to operate off
    recipes_to_process = [item for item in filtered_recipe_list]
    processed_recipes = get_all_required_recipes(recipes_to_process, filtered_item_list, recipe_list)

    service = google_sheets_connector.authenticate_google_sheets()

    items_to_write = []

    for item in sorted(filtered_item_list):
        item_entry = import_item.get_item_entry_for_item(item_list, item)
        items_to_write.append(item_entry)

    if args.write_gsheet:
        print("Writing to external spreadsheet...")
        google_sheets_connector.write_items_to_external_spreadsheet(items_to_write, service, config)
        google_sheets_connector.write_recipe_info_to_external_spreadsheet(processed_recipes, service, config)
        google_sheets_connector.write_recipe_materials_to_external_spreadsheet(processed_recipes, service, config)
        print("Done writing to spreadsheet!")

    if args.debug:
        create_local_csvs(game_version, items_to_write, processed_recipes)

if __name__ == "__main__":
    main()
