from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import dp
from copart_lot_parser import get_lot_info
from Iaai_parser import get_iaai_lot_info

class AuctionState(StatesGroup):
    choosing_auction = State()
    entering_lot = State()

@dp.message_handler(commands=["start", "lot"])
async def choose_auction(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Copart", "IAAI")
    await message.answer("Оберіть аукціон:", reply_markup=kb)
    await AuctionState.choosing_auction.set()

@dp.message_handler(state=AuctionState.choosing_auction)
async def ask_lot_number(message: types.Message, state: FSMContext):
    auction = message.text.strip().lower()
    if auction not in ["copart", "iaai"]:
        return await message.answer("❗️Будь ласка, оберіть Copart або IAAI")

    await state.update_data(auction=auction)
    await message.answer("Введіть номер лота:", reply_markup=types.ReplyKeyboardRemove())
    await AuctionState.entering_lot.set()

@dp.message_handler(state=AuctionState.entering_lot)
async def parse_lot(message: types.Message, state: FSMContext):
    lot_id = message.text.strip()
    if not lot_id.isdigit():
        return await message.answer("❗️Номер лота має бути числом")

    data = await state.get_data()
    auction = data.get("auction")
    await state.finish()

    await message.answer(f"🔍 Шукаю інформацію по лоту {lot_id}...")

    if auction == "copart":
        result = get_lot_info(lot_id)
    else:
        print("👉 запуск IAAI парсера")
        result = await get_iaai_lot_info(lot_id)
        print("✅ парсинг завершено")

    await message.answer(result, parse_mode="HTML")