from time import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.adminKeyboard import adminButton, back
from loader import dp
from states.adminState import AdminState
from utils.db_api.model import getUserList, getUsersCount, create_template, del_admin_user, get_template
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands='admin')
async def admin_panel(msg: types.Message):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.reply(f"{msg.from_user.full_name} Admin panelga hush kelibsiz!", reply_markup=adminButton)
        await AdminState.adminState.set()
    else:
        await msg.reply("Siz noto'g'ri buyruq kiritdingiz!")

@dp.message_handler(text="Adminni olib tashlash",state=AdminState.adminState)
async def del_admin(message:types.Message):
    await message.answer("Olib tashlanadigan <b>Admin Id</b> sini kiriting!")
    await AdminState.delAdmin.set()


@dp.message_handler(text="shablon qo'shish",state=AdminState.adminState)
async def add_template(message:types.Message):
    await message.answer("👮‍♂Ассалому алайкум #{full_name}\n\n📲 Сизнинг хабарингиз ишончли шаферларга етказилди ✅\n\n🕐 Тез орада сиз билан богланишади 🚕\n\n🛣 Йулингиз бехатар булсин🤲\n\n🧑‍💻Админ билан боғланиш:  @akramov_1100")
    await message.answer("Shablon quyidagi shaklga o'xshash bo'lishi shart! <b>{full_name}</b> shuni doim qo'shib keting!")
    await AdminState.template.set()

@dp.message_handler(content_types=['text'],state=AdminState.template)
async def add_template(message:types.Message,state:FSMContext):
    if message.text.find('{full_name}')==-1:
        await message.answer("Shablon xato\n\nShablonda {full_name} bo'lishi shart\nQayta yuboring!")
        return
    else:
        try:
            await create_template(context=message.text)
            await message.answer("Yangi shablon yaratildi!",reply_markup=adminButton)
        except:
            await message.answer("Xatolik yuz berdi template qo'shishda",reply_markup=adminButton)
    await AdminState.adminState.set()


@dp.message_handler(content_types=['text'],state=AdminState.delAdmin)
async def del_admin(message:types.Message):
    try:
        await del_admin_user(message.text)
        await message.answer(f"ID:{message.text} Admin olib tashlandi!✅")
    except:
        await message.answer("Xatolik yuz berdi,Admin bazada mavjud emas!")
    await AdminState.adminState.set()

@dp.message_handler(text="Userlarga Xabar yuborish", state=AdminState.adminState)
async def send_users(msg: types.Message):
    await AdminState.next()
    await msg.reply("Userlarga yuboriladigan habarni kiriting!", reply_markup=back)


@dp.message_handler(text="Guruhlarga Xabar yuborish", state=AdminState.adminState)
async def send_users(msg: types.Message):
    await AdminState.SendGroups.set()
    await msg.reply("Gruhlarga yuboriladigan habarni kiriting!", reply_markup=back)


@dp.message_handler(text="Statistika", state=AdminState.SendUsers)
@dp.message_handler(text="Statistika", state=AdminState.adminState)
@dp.message_handler(text="Statistika", state=AdminState.SendGroups)
async def user_statistic(msg: types.Message):
    users = await getUsersCount("0")
    groups = await getUsersCount("1")
    await msg.answer(f"<b>📊 Bot Statistikasi \n\n 👤 Members: {users}\n👥 groups: {groups}</b>")


@dp.message_handler(state=AdminState.adminState, text="🔙chiqish")
@dp.message_handler(state=AdminState.SendUsers, text="🔙chiqish")
@dp.message_handler(state=AdminState.SendGroups, text="🔙chiqish")
async def exit_admin(msg: types.Message, state: FSMContext):
    await msg.answer("Admin paneldan chiqdingiz!", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=AdminState.SendUsers, text="🔙ortga")
@dp.message_handler(state=AdminState.SendGroups, text="🔙ortga")
async def exit_admin(msg: types.Message, state: FSMContext):
    await msg.answer("Orga qaytildi", reply_markup=adminButton)
    await AdminState.adminState.set()


@dp.message_handler(state=AdminState.SendUsers, content_types=types.ContentTypes.ANY)
async def send_users(msg: types.Message):
    reply_markup = msg.reply_markup
    rows = await getUserList("0")
    count = 0
    for row in rows:
        try:
            await msg.bot.copy_message(row.chat_id, msg.from_user.id, msg.message_id, reply_markup=reply_markup)
            count += 1
        except:
            pass
        sleep(0.07)
    await msg.reply(f"{count} ta foydalanuvchilarga habar yuborildi")


@dp.message_handler(state=AdminState.SendGroups, content_types=types.ContentTypes.ANY)
async def send_users(msg: types.Message):
    reply_markup = msg.reply_markup
    rows = await getUserList("1")
    count = 0
    for row in rows:
        try:
            await msg.bot.copy_message(row.chat_id, msg.from_user.id, msg.message_id, reply_markup=reply_markup)
            count += 1
        except:
            pass
        sleep(0.07)
    await msg.reply(f"{count} ta Gruhlarga habar yuborildi")
