from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import dp
from copart_lot_parser import get_lot_info
from iaai_parser import fetch_iaai_info
import re

class AuctionState(StatesGroup):
    choosing_auction = State()
    entering_url = State()

def extract_lot_id_from_copart(url: str) -> str:
    match = re.search(r'/lot/(\d+)', url)
    return match.group(1) if match else None

@dp.message_handler(commands=["start", "lot"])
async def choose_auction(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Copart", "IAAI")
    await message.answer("Оберіть аукціон:", reply_markup=kb)
    await AuctionState.choosing_auction.set()

@dp.message_handler(state=AuctionState.choosing_auction)
async def ask_link(message: types.Message, state: FSMContext):
    auction = message.text.strip().lower()
    if auction not in ["copart", "iaai"]:
        return await message.answer("❗ Будь ласка, оберіть Copart або IAAI")
    await state.update_data(auction=auction)
    await message.answer("Вставте посилання на лот:", reply_markup=types.ReplyKeyboardRemove())
    await AuctionState.entering_url.set()

@dp.message_handler(state=AuctionState.entering_url)
async def parse_lot_link(message: types.Message, state: FSMContext):
    url = message.text.strip()
    data = await state.get_data()
    auction = data.get("auction")
    await state.finish()

    await message.answer("🔍 Обробляю посилання...")

    if auction == "copart":
        lot_id = extract_lot_id_from_copart(url)
        if not lot_id:
            return await message.answer("❗ Не вдалося витягнути номер лота з посилання")
        result = get_lot_info(lot_id)
    else:
        result = fetch_iaai_info(url)

    if isinstance(result, dict):
        msg = "\n".join([f"<b>{k}</b>: {v}" for k, v in result.items()])
    else:
        msg = result

    await message.answer(msg, parse_mode="HTML")