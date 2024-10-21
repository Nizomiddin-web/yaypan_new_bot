from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default.adminKeyboard import registerbtn
from loader import dp, bot
from states.adminState import AdminState
from states.userState import GroupState, Registration
from utils.db_api.model import new_user_add, new_group_add, get_user


@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE))
@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE), state=GroupState.add_group)
@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE), state=Registration.waiting_for_name)
@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    state=Registration.waiting_for_surname)
@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE),
                    state=Registration.waiting_for_phone)
async def show_channels(message: types.Message, state: FSMContext):
    try:
        await new_user_add(message.from_user.id, "0")
    except:
        pass
    text = f"<b>Assalomu alaykum, {message.from_user.first_name}</b>"
    await message.answer(text, reply_markup=registerbtn)
    await state.finish()

@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.SUPERGROUP))
async def show_channels(message: types.Message):
    text = f"<b>Assalomu alaykum, {message.from_user.first_name}</b>"
    try:
        await new_user_add(message.chat.id, "1")
        await message.answer(text)
    except:
        await message.answer(text)


@dp.message_handler(text="registratsiya")
async def cmd_start(message: types.Message):
    try:
        user = await get_user(message.from_user.id)
        if user is None:
            await message.reply("Ismingizni kiriting:",reply_markup=ReplyKeyboardRemove())
            await Registration.waiting_for_name.set()
        else:
            await message.answer("Siz ro'yhatdan o'tgansiz!")
    except:
        pass


@dp.message_handler(text="guruh qo'shish", state=AdminState.adminState)
async def add_group(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer(
            "<b>Qaysi guruhga habarlar yuborilsin?\nHabar yuboriladigan guruh id sini yozing!</b> \n❗️Eslatma Bot guruhda admin bo'lishi shart!!!",
            reply_markup=ReplyKeyboardRemove())
        await GroupState.send_group.set()
    else:
        await message.answer("Siz guruhlarni qo'sha olmaysiz!!!")


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE), state=GroupState.send_group, content_types=['text'])
async def add_group(message: types.Message, state: FSMContext):
    try:
        member = await bot.get_chat_member(chat_id=message.text, user_id=(await bot.me).id)
        if (member.status == 'administrator'):
            await message.answer("bot guruh admini")
            chat = await bot.get_chat(message.text)
            try:
                if message.text.startswith("-100"):
                    chat_id = message.text
                else:
                    chat_id = f"-100{message.text}"
                await new_group_add(f"{chat_id}",chat.title)
                await message.answer("Guruh qo'shildi!!!")
            except:
                await message.answer("Guruh qo'shilmadi qaytadan urinib ko'ring!!!")
        elif (member.status == 'member'):
            await message.answer("Bot guruh a'zosi\nBotni qo'shish uchun admin qilishingiz shart!")
    except:
        await message.answer("Bot bu guruhda mavjud emas!!!")
    await state.finish()

# Guruhga bot qo'shilganda yoki olib tashlanganda ishlaydigan handler
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def on_bot_added(message: types.Message):
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if new_member.id == (await bot.me).id:
                if str(message.from_user.id) not in ADMINS:
                    await bot.leave_chat(message.chat.id)
                    return
                try:
                    await new_user_add(message.chat.id, "1")
                except:
                    pass
                title = f"<a href='tg://user?id={message.chat.id}'>{message.chat.title}</a>"
                text = f"<b>Bot guruhga qo'shildi!!!\n\nGuruh: {title}\nGuruh ID: <code>{message.chat.id}</code>\nGuruh turi:{message.chat.type}\nFoydalanuvchi soni:{await message.chat.get_member_count()}</b>"
                await message.bot.send_message(ADMINS[1], text)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def on_bot_removed(message: types.Message):
    if message.left_chat_member.id == (await bot.me).id:
        pass
        # if message.chat.id in joined_groups:
        #     joined_groups.remove(message.chat.id)
        #     await message.reply("Bot guruhdan olib tashlandi!")
