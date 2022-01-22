from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_keyboard(skin_id):
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Купить', callback_data=f'buy:{skin_id}')
                                        ]
                                    ])
    return keyboard


paid_keyboard = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Оплатил', callback_data='paid'),
                                             InlineKeyboardButton(text='Отмена', callback_data='back_up_call')
                                         ]
                                     ])
