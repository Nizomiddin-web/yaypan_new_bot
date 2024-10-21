from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

adminButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Userlarga Xabar yuborish"),
            KeyboardButton(text="Guruhlarga Xabar yuborish"),
        ],
        [
            KeyboardButton(text="guruh qo'shish"),
            KeyboardButton(text="Statistika")
        ],
        [
            KeyboardButton(text="shablon qo'shish"),
            KeyboardButton(text="Adminni olib tashlash")
        ],
        [
            KeyboardButton(text="🔙chiqish")
        ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙ortga")
        ]
    ],
    resize_keyboard=True
)

registerbtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="registratsiya")
        ]
    ],
    resize_keyboard=True
)