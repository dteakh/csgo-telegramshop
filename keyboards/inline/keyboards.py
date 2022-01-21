from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Дальше', callback_data='continue')
                                          ]
                                      ])
accept_policy = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Согласиться', callback_data='accept')
                                         ]
                                     ])
suggest_reg_keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text='Зарегистрироваться',
                                                                         callback_data='register'),
                                                    InlineKeyboardButton(text='Пропустить', callback_data='menu')
                                                ]
                                            ])
menu_keyboard = InlineKeyboardMarkup(row_width=3,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Каталог',
                                                                  callback_data='catalog'),
                                             InlineKeyboardButton(text='Профиль',
                                                                  callback_data='profile'),
                                             InlineKeyboardButton(text='Инструкция',
                                                                  callback_data='guidance')
                                         ],
                                         [
                                             InlineKeyboardButton(text='Отзывы',
                                                                  callback_data='feedbacks'),
                                             InlineKeyboardButton(text='Важно',
                                                                  callback_data='policy'),
                                             InlineKeyboardButton(text='Связь',
                                                                  callback_data='socials')
                                         ]
                                     ])
back_up_button = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                          ]
                                      ])
update_link = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Изменить', callback_data='update_link'),
                                           InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                       ]
                                   ])
profile_keyboard = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Регистрация', callback_data='register'),
                                                InlineKeyboardButton(text='Корзина', callback_data='cart')
                                            ],
                                            [
                                                InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                            ]
                                        ])
feedback_keyboard = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(text='Читать', callback_data='read_feedbacks'),
                                                 InlineKeyboardButton(text='Оценить', callback_data='rate')
                                             ],
                                             [
                                                 InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                             ]
                                         ])
rating_keyboard = InlineKeyboardMarkup(row_width=2,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text='Ужасно 🤦‍', callback_data='rating_one'),
                                               InlineKeyboardButton(text='Плохо 😕', callback_data='rating_two')
                                           ],
                                           [
                                               InlineKeyboardButton(text='Хорошо ☺', callback_data='rating_three'),
                                               InlineKeyboardButton(text='Отлично 🤩', callback_data='rating_four')
                                           ],
                                           [
                                               InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                           ]
                                       ])
update_fb_keyboard = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Изменить', callback_data='update_fb'),
                                                  InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                              ]
                                          ])
set_feedback_text = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(text='Написать', callback_data='write_text'),
                                                 InlineKeyboardButton(text='Назад', callback_data='back_up_call')
                                             ]
                                         ])
