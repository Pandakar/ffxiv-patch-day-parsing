import os
import pickle
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from lib.item import Item

# This is more for what I'm doing with this specific application.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def authenticate_google_sheets():
    """
    Use locally stored credentials to connect to desired Google Sheet.

    Inspired and borrowed from the following link:
    https://developers.google.com/sheets/api/quickstart/python.

    credentials.json is not included as part of this repository.
    See above for a way of getting this file for yourself.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def clear_sheet(service, sheet_range, spreadsheet_id):
    """
    Remove all data from given spreadsheet.
    Precursor to repopulating a spreadsheet.
    """
    spreadsheet = service.spreadsheets()
    request = spreadsheet.values().clear(spreadsheetId=spreadsheet_id,
                                         range=sheet_range)
    response = request.execute()
    if response["spreadsheetId"] != spreadsheet_id:
        print(F"*** ERROR! Attempted to clear sheet {spreadsheet_id}, but got the following: ")
        print(response)
        sys.exit(1)


def write_items_to_external_spreadsheet(item_list, service, config):
    spreadsheet_id = config["spreadsheet_id"]
    item_range = config["item_range"]
    """
    Write relevant items to external spreadsheet.
    """
    header_row = Item().__dict__.keys()

    data = [list(header_row)] + [item.to_sheet_row() for item in item_list]
    # First, clear out data from sheet
    clear_sheet(service, item_range, spreadsheet_id)

    value_input_option = 'RAW'
    insert_data_option = 'OVERWRITE'
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': data
    }

    spreadsheet_values = service.spreadsheets().values()
    request = spreadsheet_values.append(spreadsheetId=spreadsheet_id,
                                        range=item_range,
                                        valueInputOption=value_input_option,
                                        insertDataOption=insert_data_option,
                                        body=value_range_body)
    response = request.execute()

    if response["spreadsheetId"] != spreadsheet_id:
        print("Didn't get correct spreadsheet, see following response")
        print(response)
        sys.exit(1)

    num_rows_updated = response["updates"]["updatedRows"]

    if num_rows_updated != len(data):
        print(F"Error with writing data, expected to write {len(data)} rows but only wrote {num_rows_updated} rows.")
        print(response)
        sys.exit(2)


def write_recipe_materials_to_external_spreadsheet(recipe_list, service, config):
    spreadsheet_id = config["spreadsheet_id"]
    recipe_materials_range = config["recipe_materials_range"]
    data = []
    header = ["recipe_name", "material", "amount"]
    for recipe in recipe_list:
        for ingredient, amount in recipe.ingredients:
            row = {"recipe_name": recipe.item_result.strip(),
                   "material": ingredient.strip(),
                   "amount": amount.strip()}
            data.append(row)

    write_data = [header] + [list(entry.values()) for entry in data]
    clear_sheet(service, recipe_materials_range, spreadsheet_id)

    value_input_option = 'RAW'
    insert_data_option = 'OVERWRITE'
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': write_data
    }

    spreadsheet_values = service.spreadsheets().values()
    request = spreadsheet_values.append(spreadsheetId=spreadsheet_id,
                                        range=recipe_materials_range,
                                        valueInputOption=value_input_option,
                                        insertDataOption=insert_data_option,
                                        body=value_range_body)
    response = request.execute()

    if response["spreadsheetId"] != spreadsheet_id:
        print("Didn't get correct spreadsheet, see following response")
        print(response)
        sys.exit(1)

    num_rows_updated = response["updates"]["updatedRows"]

    if num_rows_updated != len(write_data):
        print(F"Error with writing data, expected to write {len(write_data)} rows but only wrote {num_rows_updated} rows.")
        print(response)
        sys.exit(2)


def write_recipe_info_to_external_spreadsheet(recipe_list, service, config):
    spreadsheet_id = config["spreadsheet_id"]
    recipe_info_range = config["recipe_info_range"]
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

    write_data = [header] + [list(entry.values()) for entry in data]
    clear_sheet(service, recipe_info_range, spreadsheet_id)

    value_input_option = 'RAW'
    insert_data_option = 'OVERWRITE'
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': write_data
    }

    spreadsheet_values = service.spreadsheets().values()
    request = spreadsheet_values.append(spreadsheetId=spreadsheet_id,
                                        range=recipe_info_range,
                                        valueInputOption=value_input_option,
                                        insertDataOption=insert_data_option,
                                        body=value_range_body)
    response = request.execute()

    if response["spreadsheetId"] != spreadsheet_id:
        print("Didn't get correct spreadsheet, see following response")
        print(response)
        sys.exit(1)

    num_rows_updated = response["updates"]["updatedRows"]

    if num_rows_updated != len(write_data):
        print(F"Error with writing data, expected to write {len(write_data)} rows but wrote {num_rows_updated} rows.")
        print(response)
        sys.exit(2)
