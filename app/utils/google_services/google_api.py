from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.utils.google_services.services import (get_google_drive_service,
                                                get_google_sheet_service)

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await get_google_sheet_service(wrapper_services)
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт от {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'row_count': 100,
                    'column_count': 11
                }
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheetid)
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await get_google_drive_service(wrapper_services)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    charity_projects: list,
    wrapper_services: Aiogoogle,
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await get_google_sheet_service(wrapper_services)
    table_values = [
        ['Отчет от ', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for charity_project in charity_projects:
        new_charity_project = [
            str(charity_project['name']),
            str(timedelta(seconds=charity_project['fundraising'])),
            str(charity_project['description']),
        ]
        table_values.append(new_charity_project)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )