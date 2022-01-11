import logging

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeEdited
from django.db import IntegrityError

from app import dp
from utils.db_api.db_commands import add_user


@dp.message_handler(commands='start')
async def start(message: Message):
    try:
        await message.delete_reply_markup()
    except MessageCantBeEdited:
        pass
    try:
        await add_user(user_id=message.from_user.id)
    except IntegrityError as ex:
        logging.info(f'Пользователь {message.from_user.id} уже зарегистрирован')
    await message.answer('Привет')
