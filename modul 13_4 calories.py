from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
	age = State()
	growth = State()
	weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
	print(
		'Hello! I am bot and can assist you with health issues.'
		'I am able to count calories for women.'
		'Print ok if still interested.'
	)
	await message.answer(
		'Hello! I am bot and can assist you with health issues.'
		'I am able to count calories for women.'
		'Print ok if still interested.'
	)


@dp.message_handler(text=['ok'])
async def count(message):
	print('Print Calories, to initiate our communication.')
	await message.answer('Print Calories, to initiate our communication.')


@dp.message_handler(text='Calories')
async def set_age(message):
	await message.answer(f'Enter your age')
	await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
	await state.update_data(age=message.text)
	await message.answer(f'Enter your growth in sm')
	await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
	await state.update_data(growth=message.text)
	await message.answer(f'Enter your weight in kg')
	await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
	await state.update_data(weight=message.text)
	data = await state.get_data()
	results = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
	await message.answer(f'Your normal amount of calories per day is {results}')
	await state.finish()


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)

# для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161

# @dp.message_handler(state=UserState.address)
# async def fsm_handler(message, state):
# 	await state.update_data(first=message.text)
# 	data = await state.get_data()
# 	await message.answer(f'Delivery will be dispatched to {data["first"]}')
# 	await state.finish()

# @dp.message_handler(text='Delivery')
# async def buy(message):
# 	await message.answer('Send us your address')
# 	await UserState.address.set()

# @dp.message_handler(text = ['Urban', 'ff'])
# async def urban_message(message):
# 	print('Urban message')
#
# @dp.message_handler(commands=['start'])
# async def start_message(message):
# 	print('Start message')

# @dp.message_handler()
# async def all_message(message):
# 	print('Мы получили сообщение!')

# class UserState(StatesGroup):
# 	address = State()
#
# @dp.message_handler(text='Delivery')
# async def buy(message):
# 	await message.answer('Send us your address')
# 	await UserState.address.set()
#
# @dp.message_handler(state=UserState.address)
# async def fsm_handler(message, state):
# 	await state.update_data(first=message.text)
# 	data = await state.get_data()
# 	await message.answer(f'Delivery will be dispatched to {data["first"]}')
# 	await state.finish()
