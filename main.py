from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await message.answer("Привет! Для расчета нормы калорий отправьте сообщение 'Calories'.")

@dp.message_handler(text='Calories')
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст (число).")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный рост (число в см).")
        return
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный вес (число в кг).")
        return
    await state.update_data(weight=int(message.text))  # Сохраняем вес

    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Норма калорий для вашего возраста, роста и веса: {calories:.2f} калорий в день.")

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
