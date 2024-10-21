from aiogram.dispatcher import filters
from aiogram import types
from loader import dp, bot
from utils.db_api.model import get_group, get_user, get_template


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.SUPERGROUP), content_types=['text'])
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP), content_types=['text'])
async def echo(message: types.Message):
    try:
        group = await get_group()
        user = await get_user(message.from_user.id)
        template = await get_template()
        context = template.content.format(full_name=message.from_user.full_name)
        if message.chat.id != group.chat_id:
            if user:
                pass
            else:
                if message.chat.username:
                    group_link = f"https://t.me/{message.chat.username}"
                else:
                    group_link = f"#"
                group_link = f"<a href='{group_link}'>{message.chat.title}</a>"
                text = message.text
                text = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\n{text}\n\n{group_link}"
                await message.bot.send_message(group.chat_id, text)
                await message.delete()
                await message.answer(context)
    except Exception as e:
        pass

