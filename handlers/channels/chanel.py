from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from data.config import ADMINS
from loader import dp, bot
from states.adminState import AdminState
from states.userState import GroupState
from utils.db_api.model import new_user_add, send_users_add, getUserList, get_user

CHANNEL_ID = -1002165597882
#CHANNEL_ID = -1001810259321
class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_phone = State()





@dp.message_handler(state=Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Familiyangizni kiriting:")
    await Registration.waiting_for_surname.set()


@dp.message_handler(state=Registration.waiting_for_surname)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.reply("Telefon raqamingizni kiriting:")
    await Registration.waiting_for_phone.set()


@dp.message_handler(state=Registration.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    surname = user_data['surname']
    phone = message.text

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text="Tasdiqlash", callback_data=f"Yes_{message.from_user.id}"),
               InlineKeyboardButton(text="Bekor qilish", callback_data=f"No_{message.from_user.id}")]
    keyboard.add(*buttons)
    await bot.send_message(CHANNEL_ID,
                           f"<b>Ro'yxatdan o'tish so'rovi:</b>\n\nIsm: {name}\nFamiliya: {surname}\nTelefon: {phone}",
                           reply_markup=keyboard)
    await message.reply("Ro'yxatdan o'tish so'rovi yuborildi. Admin tasdiqlashini kuting.")
    await state.finish()


@dp.callback_query_handler()
async def process_admin_response(message: types.CallbackQuery):
    if str(message.from_user.id) in ADMINS:
        if message.data.startswith("Yes"):
            user_id = message.data.split("_")[1]
            try:
                await send_users_add(user_id)
            except:
                pass
            text = f"{message.message.text}\n\n<b>Status: ✅Tasdiqlandi✅</b>"
            await message.message.edit_text(text)
            await message.bot.send_message(chat_id=user_id,
                                           text="Tasdiqlandingiz! Guruhda yozishingiz mumkin!!!.")
        else:
            user_id = message.data.split("_")[1]
            text = f"{message.message.text}\n\n<b>Status: ❌Rad Etildi❌</b>"
            await message.message.edit_text(text)
            await message.bot.send_message(chat_id=user_id, text="Rad etildingiz.")

