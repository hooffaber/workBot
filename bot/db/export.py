import os
from datetime import datetime
from typing import Any
import pandas as pd

DATA_FOLDER = 'data/export/'


def export_data(query_data: Any, export_time: str):
    export_data_list = []
    for work_hour, fullname, obj_name, worked_hours, description in query_data:
        start_time = work_hour.startTime.strftime("%Y-%m-%d %H:%M:%S")
        finish_time = work_hour.finishTime.strftime("%Y-%m-%d %H:%M:%S") if work_hour.finishTime else ""
        address = work_hour.address

        export_data_list.append(
            [fullname, start_time, finish_time, address, f"{obj_name} - {worked_hours}, - {description}"])

    df = pd.DataFrame(export_data_list, columns=['Fullname', 'StartTime', 'FinishTime', 'Address', 'FacilityData'])

    file_name = f"exported_data_{export_time}_{datetime.now().strftime('%d_%m_%H%M%S')}.xlsx"

    if check_folders(DATA_FOLDER):
        filepath = os.path.join(DATA_FOLDER, file_name)
        df.to_excel(filepath, index=True)
        print(f"Data exported successfully to {file_name}")
        return filepath

    return None


def check_folders(path: str):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as e:
        print(f"While creating folders {path} there's an error: {e}")
