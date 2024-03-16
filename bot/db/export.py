import os
from datetime import datetime
from typing import Any

import pandas as pd
import gspread

from oauth2client.service_account import ServiceAccountCredentials

from bot.db.orm import summarize_worked_hours

DATA_FOLDER = 'data/export/'


def export_excel_data(query_data: Any, export_time: str):
    export_data_list = []
    for work_hour, fullname, obj_name, worked_hours, description in query_data:
        start_time = work_hour.startTime.strftime("%Y-%m-%d %H:%M:%S")
        finish_time = work_hour.finishTime.strftime("%Y-%m-%d %H:%M:%S") if work_hour.finishTime else ""
        address = work_hour.address
        finish_address = work_hour.finish_address

        export_data_list.append(
            [fullname, start_time, finish_time, address, finish_address, obj_name, worked_hours, description])

    df = pd.DataFrame(export_data_list,
                      columns=['Fullname', 'StartTime', 'FinishTime', 'Address', 'FinishAddress', 'FacilityData'])

    file_name = f"exported_data_{export_time}_{datetime.now().strftime('%d_%m_%H%M%S')}.xlsx"

    if check_folders(DATA_FOLDER):
        filepath = os.path.join(DATA_FOLDER, file_name)
        df.to_excel(filepath, index=True)
        print(f"Data exported successfully to {file_name}")
        return filepath

    return None


def export_data_to_google_sheets(query_data: Any, export_time: str, spreadsheet_name: str, worksheet_name: str):
    CREDENTIALS_FILE = 'google_api/upheld-ellipse-417216-ee26838eef4f.json'  # имя файла с закрытым ключом
    SPREADSHEET_NAME = "workBot"
    SHEET_TITLE = "workBotSheet"

    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.create(SPREADSHEET_NAME)

    spreadsheet.share(None, perm_type='anyone', role='reader')

    worksheet = spreadsheet.get_worksheet(0)

    if worksheet.title != SHEET_TITLE:
        worksheet.update_title(SHEET_TITLE)

    export_data_list = [
        ["ФИО", "Время начала", "Время окончания", "Адрес старта", "Конечный адрес", "Название объекта", "Время", "Описание"]]
    for work_hour, fullname, obj_name, worked_hours, description in query_data:
        start_time = work_hour.startTime.strftime("%Y-%m-%d %H:%M:%S")
        finish_time = work_hour.finishTime.strftime("%Y-%m-%d %H:%M:%S") if work_hour.finishTime else ""
        address = work_hour.address
        finish_address = work_hour.finish_address
        export_data_list.append(
            [fullname, start_time, finish_time, address, finish_address, obj_name, str(worked_hours) + ' ч.', description])

    worksheet.update('A1', export_data_list)

    if export_time == 'month':
        all_values = worksheet.get_all_values()
        last_row = len(all_values)

        summary = summarize_worked_hours()
        data_for_sheets = [['']]
        for objectName, workers in summary.items():
            row = [objectName] + [fullname for fullname in workers.keys()]
            data_for_sheets.append(row)
            row = [''] + [str(hours) + ' ч.' for hours in workers.values()]
            data_for_sheets.append(row)

        worksheet.update(f'A{last_row + 2}', data_for_sheets)

    return spreadsheet.url


def check_folders(path: str):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as e:
        print(f"While creating folders {path} there's an error: {e}")
