import gspread
from google.oauth2.service_account import Credentials
import json
import os
from config import config

class Sheet:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(config.CREDENTIALS_JSON, scopes=scopes)
        client = gspread.authorize(creds)

        workbook = client.open_by_key(config.SHEET_ID)

        worksheet_list = map(lambda x: x.title, workbook.worksheets())
        if config.DATE_TIME in worksheet_list:
            self.sheet = workbook.worksheet(config.DATE_TIME)
        else:
            self.sheet = workbook.add_worksheet(config.DATE_TIME, rows=20, cols=20)

        self.data_json = os.path.join(config.MATCH_LOG, f'{config.DATE_TIME}.json')
        if not os.path.exists(self.data_json):
            self.data = {}
            for name in config.members:
                self.data[name] = {}
                for parameters in config.parameters:
                    self.data[name][parameters] = 0
            with open(self.data_json, 'w', encoding="utf-8") as new_file:
                json.dump(self.data, new_file)
        else:
            with open(self.data_json, 'r', encoding="utf-8") as file:
                self.data = json.load(file)

        self.values = self.data_to_sheet()

        # Get match score position in sheet
        self.match_score_sheet = workbook.worksheet("Match_Score")
        # Get the last element with a character in column A
        col_a_values = self.match_score_sheet.col_values(1)
        last_row = len(col_a_values)
        while last_row > 0 and not col_a_values[last_row - 1].strip():
            last_row -= 1

        # Check if the last element matches config.DATE_TIME
        if last_row > 0 and col_a_values[last_row - 1] == config.DATE_TIME:
            self.match_score_row = last_row
        else:
            self.match_score_row = last_row + 1
            self.match_score_sheet.update_cell(self.match_score_row, 1, config.DATE_TIME)

        # Collect and update match score
        with open(config.MATCH_SCORE_JSON, 'r', encoding='utf-8') as file:
            match_score_json = json.load(file)
        if config.DATE_TIME not in match_score_json:
            self.match_score = "0 - 0"
        else:
            self.match_score = match_score_json[config.DATE_TIME]
        self.update_match_core()

    def data_to_sheet(self):
        self.sheet.clear()

        # Data to values
        values = [name for name in self.data]
        values.insert(0, "")
        values = [values]
        for parameter in config.parameters:
            member_data = [parameter]
            for name in self.data:
                member_data.append(self.data[name][parameter])
            values.append(member_data)

        # Update values to the sheet
        column_letter = self.number_to_column_letter(len(values[0]))
        row_number = len(values)
        self.sheet.update(f"A1:{column_letter}{row_number}", values)
        self.sheet.format(f"A1:{column_letter}1", {"textFormat": {"bold": True}})

        # Update point calculations
        row_number = len(values) + 1
        for column_number in range(2, len(values[0]) + 1):
            column_letter = self.number_to_column_letter(column_number)
            command = "=sum("
            for row in range(2, row_number):
                parameter = values[row-1][0]
                weight = str(config.parameters[parameter]["weight"]).replace('.',',')
                command += f"{column_letter}{row}*({weight})+"
            command = command[:-1] + ")"
            self.sheet.update_cell(row_number, column_number, command)

        return values

    def number_to_column_letter(self, n):
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string
    
    def update_match_core(self):
        self.match_score_sheet.update_cell(self.match_score_row, 2, self.match_score)

    def update(self, name, name_id, parameter, parameter_id, match_score):
        if name is not None:
            row_number = parameter_id + 1
            column_number = name_id + 1
            # Update self.values
            self.values[row_number-1][column_number-1] += 1
            # Update the sheet
            self.sheet.update_cell(row_number, column_number, self.values[row_number-1][column_number-1])
            # Update the data
            self.data[name][parameter] += 1
            with open(self.data_json, 'w') as file:
                json.dump(self.data, file)

        # Update match score
        if match_score != self.match_score:
            self.match_score = match_score
            self.update_match_core()
    
    def remove_latest(self, name, name_id, parameter, parameter_id, match_score):
        if name is not None:
            row_number = parameter_id + 1
            column_number = name_id + 1
            # Update self.values
            self.values[row_number-1][column_number-1] -= 1
            # Update the sheet
            self.sheet.update_cell(row_number, column_number, self.values[row_number-1][column_number-1])
            # Update the data
            self.data[name][parameter] -= 1
            with open(self.data_json, 'w') as file:
                json.dump(self.data, file)

        # Update match score
        if match_score != self.match_score:
            self.match_score = match_score
            self.update_match_core()

# update = Sheet()
