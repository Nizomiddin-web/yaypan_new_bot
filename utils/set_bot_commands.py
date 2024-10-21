from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            # types.BotCommand("registratsiya","Haydovchi sifatida ro'yhatdan o'tish")
            # types.BotCommand("help", "yordam"),
            # types.BotCommand("menu", "asosiy menuga o'tish"),
            # types.BotCommand("data", "Shahsiy ma'lumotlaringiz")
        ]
    )
