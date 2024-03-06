from aiogram.filters.callback_data import CallbackData

class AdminMenuCallbackFactory(CallbackData, prefix='admin'):
    action: str

