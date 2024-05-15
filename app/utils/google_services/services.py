from aiogoogle import Aiogoogle


def get_google_sheet_service(wrapper_services: Aiogoogle):
    return wrapper_services.discover('sheets', 'v4')


def get_google_drive_service(wrapper_services: Aiogoogle):
    return wrapper_services.discover('drive', 'v3')