# Python модули
import aiosqlite


# Локальные модули
from utilities.logger import logger


# Классы
class SQLiteDB:
	def __init__(self, db_name):
		self.db_name = db_name
		self.connection = None

	async def connect(self):
		try:
			self.connection = await aiosqlite.connect(self.db_name)
			await self.connection.execute(
				'''
					CREATE TABLE IF NOT EXISTS users 
					(date DATE, user_id INTEGER UNIQUE, is_bot BOOL, first_name TEXT, last_name TEXT, 
					username TEXT UNIQUE, language_code TEXT)
				'''
			)
			await self.connection.commit()
			return True
		except Exception as e:
			logger.error(f'USER=BOT, MESSAGE="{e}"')
			return False

	async def close(self):
		try:
			await self.connection.close()
			return True
		except Exception as e:
			logger.error(f'USER=BOT, MESSAGE="{e}"')
			return False

	async def insert(self, table: str, what: tuple, values: tuple) -> bool:
		try:
			placeholders = ','.join(['?'] * len(what))
			what = ','.join(what)

			await self.connection.execute(f'''INSERT INTO {table} ({what}) VALUES ({placeholders})''', values)
			await self.connection.commit()
			logger.debug(f'USER=BOT, MESSAGE="table={table}, what=({what}), values={values}"')
			return True
		except aiosqlite.IntegrityError:
			logger.debug(f'USER=BOT, MESSAGE="UNIQUE ALREADY EXISTS | table={table}, what=({what}), values={values}"')
			return True
		except Exception as e:
			logger.error(f'USER=BOT, MESSAGE="{e}"')
			return False

	async def select(self, table: str, what: tuple | None = None, where: tuple | None = None, values: tuple | None = None):
		try:
			if not what:
				what = '*'
			else:
				what = f'({",".join(what)})'

			if where:
				where_clause = ' AND '.join([f'{i} = ?' for i in where])
				query = f'''SELECT {what} FROM {table} WHERE {where_clause}'''
				cursor = await self.connection.execute(query, values)
			else:
				query = f'''SELECT {what} FROM {table}'''
				cursor = await self.connection.execute(query)

			rows = await cursor.fetchall()
			logger.debug(
				f'USER=BOT, MESSAGE="table={table}, what={what}, where={where}, values={values}, '
				f'result_len={len(rows)}"'
			)
			return rows
		except Exception as e:
			logger.error(f'USER=BOT, MESSAGE="{e}"')
			return []
