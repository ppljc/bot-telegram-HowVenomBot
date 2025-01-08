# Python модули
from aiogram import BaseMiddleware
from aiogram.types import *
from typing import *

import datetime


# Локальные модули
from create_bot import db


# Классы
class StandardMiddleware(BaseMiddleware):
	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: Message | CallbackQuery,
			data: Dict[str, Any]
	) -> Any:
		user = event.from_user
		data['user'] = user
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		await db.insert(
			table='users',
			what=('date', 'user_id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'),
			values=(date, user.id, user.is_bot, user.first_name, user.last_name, user.username, user.language_code)
		)
		return await handler(event, data)
