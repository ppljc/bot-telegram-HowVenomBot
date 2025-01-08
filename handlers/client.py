# Python модули
from aiogram import Router
from aiogram.types import *
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

import os
import random


# Локальные модули
from utilities.logger import logger


# Переменные
router = Router(name='client')


# Функции
@router.message(Command(commands=['start'], ignore_case=True))
async def message_start(message: Message):
	try:
		await message.delete()
		await message.answer(
			text='venom, используй через вводом @HowVenomBot'
		)

		logger.info(f'USER={message.from_user.id}, MESSAGE=""')
	except Exception as e:
		logger.error(f'USER={message.from_user.id}, MESSAGE="{e}"')


@router.inline_query()
async def inline_query(query: InlineQuery):
	try:
		builder = InlineKeyboardBuilder()
		builder.button(text='Поделись venomом! 🐾', switch_inline_query='')

		results = []
		if query.query:
			results.append(
				InlineQueryResultArticle(
					id='1',
					title=f'🐾 Насколько {query.query} venom?',
					description='В процентах 🤑',
					thumbnail_url='https://img03.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/a/d9/ad9e58393fdc6b461e98b330dc312711.jpg',
					reply_markup=builder.as_markup(),
					input_message_content=InputTextMessageContent(
						message_text=f'🐾 {query.query} на {random.randint(0, 100)}% venom!'
					)
				)
			)
		else:
			results.append(
				InlineQueryResultArticle(
					id='2',
					title='🐾 Насколько вы venom?',
					description='В процентах 🤑',
					thumbnail_url='https://img03.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/a/d9/ad9e58393fdc6b461e98b330dc312711.jpg',
					reply_markup=builder.as_markup(),
					input_message_content=InputTextMessageContent(
						message_text=f'🐾 Я на {random.randint(0, 100)}% venom!'
					)
				)
			)

		results.append(
			InlineQueryResultArticle(
				id='3',
				title='🐾 Насколько это venomенально?',
				description='В процентах 🤑',
				thumbnail_url='https://img03.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/a/d9/ad9e58393fdc6b461e98b330dc312711.jpg',
				reply_markup=builder.as_markup(),
				input_message_content=InputTextMessageContent(
					message_text=f'🐾 Это на {random.randint(0, 100)}% venomенально!'
				)
			)
		)

		results.append(
			InlineQueryResultArticle(
				id='4',
				title='🐾 Помощь',
				description='Как использовать 🤔',
				thumbnail_url='https://img03.rl0.ru/afisha/e1200x1200i/daily.afisha.ru/uploads/images/a/d9/ad9e58393fdc6b461e98b330dc312711.jpg',
				reply_markup=builder.as_markup(),
				input_message_content=InputTextMessageContent(
					message_text=(
						'Либо нажмите кнопку, прикрепленную к этому сообщению, и выберите чат, '
						'в котором вы хотите разместить сообщение, либо просто введите «@HowVenomBot» в текстовое поле.\n\n'
						'Чтобы получить персонализированное venom-сообщение, отправьте сообщение @HowVenomBot!'
					)
				)
			)
		)

		await query.answer(results=results, cache_time=0)

		logger.info(f'USER={query.from_user.id}, MESSAGE="query.query={query.query}"')
	except Exception as e:
		logger.error(f'USER={query.from_user.id}, MESSAGE="{e}"')
