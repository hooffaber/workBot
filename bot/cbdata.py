from aiogram.filters.callback_data import CallbackData


class AdminMenuCallbackFactory(CallbackData, prefix='admin'):
    action: str
    subject: str


class AdminDelCallbackFactory(CallbackData, prefix='delete'):
    name: str
    subject: str


class AdminExportFactory(CallbackData, prefix='export'):
    date: str


class WorkerPickingCallbackFactory(CallbackData, prefix='worker_pick'):
    obj_id: str
