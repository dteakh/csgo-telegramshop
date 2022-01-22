import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.utils.exceptions import MessageCantBeEdited
from aiogram.utils.markdown import hlink
from django.db import IntegrityError

from app import dp
from data import config
from data.config import ADMINS
from handlers.qiwi import Payment, NoPaymentFound, NotEnoughMoney
from keyboards.inline.keyboards import start_keyboard, accept_policy, suggest_reg_keyboard, menu_keyboard, \
    back_up_button, update_link, profile_keyboard, feedback_keyboard, rating_keyboard, update_fb_keyboard, \
    set_feedback_text, register_before_buying
from keyboards.inline.purchase import buy_keyboard, paid_keyboard
from loader import bot
from utils.db_api.db_commands import add_user, return_users_link, add_users_tlink, return_all_items, \
    return_users_purchases, get_all_feedbacks, get_users_rate, set_rating, write_feedback, get_item_info, \
    delete_item_from_items, add_item_to_purchases, get_item_price


@dp.message_handler(commands='start')
async def start(message: Message):
    try:
        await message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    try:
        await add_user(user_id=message.from_user.id)
    except IntegrityError:
        logging.info(f'Пользователь {message.from_user.id} уже зарегистрирован')
    await message.answer('Привет', reply_markup=start_keyboard)


@dp.callback_query_handler(text='continue')
async def show_policy(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Договор оферта', reply_markup=accept_policy)


@dp.callback_query_handler(text='accept')
async def suggest_reg(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer('Зарегистрируйтесь сразу или сделайте это потом',
                              reply_markup=suggest_reg_keyboard)


@dp.callback_query_handler(text='menu')
async def open_menu(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Что делаем?',
                              reply_markup=menu_keyboard)


@dp.callback_query_handler(text='register')
async def sign_up_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    link = await return_users_link(user_id=call.from_user.id)
    if link is None:
        await call.message.answer('Введите вашу трейд ссылку', reply_markup=back_up_button)
        await state.set_state('register')
    else:
        await call.message.answer(f'Вы уже зарегистрированы!\n\n'
                                  f'Текущая ссылка: {link}\n\n'
                                  'Хотите изменить данные?', reply_markup=update_link)


@dp.callback_query_handler(text='back_up_call', state='*')
async def back_up(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await state.finish()
    await call.message.answer(text='Что делаем?',
                              reply_markup=menu_keyboard)


@dp.message_handler(state='register')
async def add_users_link(message: Message, state: FSMContext):
    try:
        await message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await add_users_tlink(user_id=message.from_user.id, trade_link=message.text)
    await message.answer(text=f'Новая ссылка успешно обновлена: {message.text}', reply_markup=back_up_button)
    await state.finish()


@dp.callback_query_handler(text='update_link')
async def update_users_link(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Введите новую ссылку', reply_markup=back_up_button)
    await state.set_state('register')


@dp.callback_query_handler(text='catalog')
async def open_catalog(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    items = await return_all_items()
    for item in items:
        photo_bytes = InputFile(path_or_bytesio='project/djangoadmin/media/' + str(item.picture))
        await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes,
                             caption=f'<b># {item.id} {item.name}</b>\n'
                                     f'Качество: {item.quality}\n'
                                     f'Float: {item.item_float}\n'
                                     f'Цена: {item.price}₽\n', reply_markup=buy_keyboard(item.id))
    await call.message.answer(text=f'Всего предметов на продаже: {len(items)}', reply_markup=back_up_button)


@dp.callback_query_handler(text='profile')
async def open_profile(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    if call.from_user.username is not None:
        await call.message.answer(text=f'<b>Добро пожаловать, {call.from_user.username}!</b>\n\n'
                                       f'Зарегистрироваться или изменить трейд-ссылку можно в разделе '
                                       f'<b>«Регистрация»</b>\n\nПосмотреть список купленных вами скинов, которые еще не '
                                       f'были отправлены, можно в разделе <b>«Корзина»</b>',
                                  reply_markup=profile_keyboard)
    else:
        await call.message.answer(text=f'<b>Добро пожаловать!</b>\n\n'
                                       f'Зарегистрироваться или изменить трейд-ссылку можно в разделе '
                                       f'<b>«Регистрация»</b>\n\nПосмотреть список купленных вами скинов, которые еще не '
                                       f'были отправлены, можно в разделе <b>«Корзина»</b>',
                                  reply_markup=profile_keyboard)


@dp.callback_query_handler(text='cart')
async def show_users_purchases(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    print(1)
    items = await return_users_purchases(user_id=call.from_user.id)
    text = 'Купленные вами предметы, ожидающие отправки:\n\n'
    for item in items:
        text += f'<b>#{item.id} {item.name}</b>\n' \
                f'Цена: {item.price}₽\n' \
                f'Дата покупки: {str(item.created_at).partition(".")[0]}\n\n'
    await call.message.answer(text=text, reply_markup=back_up_button)


@dp.callback_query_handler(text='guidance')
async def open_guidance(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Инструкция', reply_markup=back_up_button)


@dp.callback_query_handler(text='feedbacks')
async def open_feedbacks(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='<b>ОТЗЫВЫ</b>\n\nОценить качество работы сервиса и написать отзыв можно в разделе '
                                   '<b>«Оценить»</b>\n\nВ разделе <b>«Читать»</b> Вы можете найти наиболее актуальные '
                                   'оценки и отзывы наших покупателей', reply_markup=feedback_keyboard)


@dp.callback_query_handler(text='read_feedbacks')
async def read_feedbacks(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    feedbacks = await get_all_feedbacks()
    text = ''
    for feedback in feedbacks:
        text += hlink(f'@{feedback.user_id}', f'tg://user?id={feedback.user_id}') + f' оставил оценку ' \
                                                                                    f'<b>{feedback.feedback_rate}:\n\n' \
                                                                                    f'«{feedback.feedback_text}»</b>\n\n\n'
    if len(feedbacks) == 0:
        return await call.message.answer(text='На данный момент у нас еще нет отзывов. Вы можете стать первым, оставив '
                                              'фидбек в разделе отзывы -> оценить', reply_markup=back_up_button)
    text += 'Это наиболее актуальные отзывы'
    await call.message.answer(text=text, reply_markup=back_up_button)


@dp.callback_query_handler(text='rate')
async def rate_bot(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    rate = await get_users_rate(user_id=call.from_user.id)
    if rate is None:
        await call.message.answer(text='Выберите наиболее подходящую оценку', reply_markup=rating_keyboard)
    else:
        await call.message.answer(text=f'Вы уже оставили оценку <b>{rate}</b>\n\n'
                                       f'Хотите изменить ее?', reply_markup=update_fb_keyboard)


@dp.callback_query_handler(text_contains='rating')
async def users_rate(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    rating = call.data.split('_')[1]
    user_id = call.from_user.id
    if rating == 'one':
        await set_rating(user_id=user_id, rate='Ужасно')
    elif rating == 'two':
        await set_rating(user_id=user_id, rate='Плохо')
    elif rating == 'three':
        await set_rating(user_id=user_id, rate='Хорошо')
    else:
        await set_rating(user_id=user_id, rate='Отлично')
    await call.message.answer(text=f'Ваша оценка успешно сохранена. Желаете ли Вы оставить текстовый отзыв?',
                              reply_markup=set_feedback_text)


@dp.callback_query_handler(text='update_fb')
async def update_feedback_text(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Выберите новую оценку', reply_markup=rating_keyboard)


@dp.callback_query_handler(text='write_text')
async def write_feedback_text(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Введите и отправьте ваш текст', reply_markup=back_up_button)
    await state.set_state('feedback')


@dp.message_handler(state='feedback')
async def read_feedback(message: Message, state: FSMContext):
    try:
        await message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await write_feedback(user_id=message.from_user.id, text=message.text)
    await message.answer(text=f'Ваш отзыв успешно сохранен:\n\n'
                              f'<b>{message.text}</b>', reply_markup=back_up_button)
    await state.finish()


@dp.callback_query_handler(text='policy')
async def open_policy(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text='Политика магазина', reply_markup=back_up_button)


@dp.callback_query_handler(text='socials')
async def open_socials(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    await call.message.answer(text=f'<b>tg: </b>' + hlink(f'@1149987360', f'tg://user?id=1149987360'),
                              reply_markup=back_up_button)


@dp.callback_query_handler(text_contains='buy')
async def create_invoice(call: CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        await call.message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    trade_link = await return_users_link(user_id=call.from_user.id)
    if trade_link is None:
        await call.message.answer(text='Перед покупкой зарегистрируйте свою трейд-ссылку',
                                  reply_markup=register_before_buying)
    else:
        skin_id = call.data.split(':')[-1]
        amount = await get_item_price(int(skin_id))
        payment = Payment(amount=int(amount))
        payment.create()
        await call.message.answer(text=f'Оплатите не менее <b>{amount} ₽</b> на QIWI: {config.QIWI_NUMBER}\n\n'
                                       f'Это можно сделать как вручную, так и кликнув по готовой ссылке: ' +
                                       hlink('оплатить', payment.invoice) + '\n\n'
                                                                            f'Главное <b>не забудьте указать комментарий</b> к оплате: '
                                                                            f'<code>{payment.payment_key}</code>\n\n'
                                                                            f'После проведения оплаты нажмите <b>«Оплатил»</b>\n'
                                                                            f'Для отмены покупки нажмите <b>«Отмена»</b>',
                                  reply_markup=paid_keyboard)
        await state.set_state('qiwi')
        await state.update_data(payment=payment, skin_id=skin_id)


@dp.callback_query_handler(text='paid', state='qiwi')
async def approve_payment(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    payment: Payment = data.get('payment')
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer(text='Платеж не найден, проверьте правильность введенных данных')
        return
    except NotEnoughMoney:
        await call.message.answer(text='Была переведена недостаточная сумма. Проверьте правильность введенных данных')
        return
    else:
        await call.message.answer(text='<b>Оплата прошла успешно.</b>\n'
                                       'Список приобретенных вами предметов можно найти в разделе '
                                       '<b>«Профиль» -> «Корзина»</b>\n\n'
                                       'В течении ближайшего времени вам будет отправлен предмет\n\n'
                                       'Спасибо за покупку, вы также можете оставить отзыв в разделе <b>«Отзывы»!</b>',
                                  reply_markup=back_up_button)
        for admin_id in ADMINS:
            await bot.send_message(chat_id=admin_id, text='Новая покупка')
        item = await get_item_info(int(data['skin_id']))
        await delete_item_from_items(int(data['skin_id']))
        await add_item_to_purchases(skin_id=item.id, name=item.name, price=item.price, buyer_id=call.from_user.id,
                                    buyer_link=return_users_link(call.from_user.id))
    await state.finish()