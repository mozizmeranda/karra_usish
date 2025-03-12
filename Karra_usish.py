from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from states import Registration
from utils import contact_save, create_contact, lead_create_without_landing
from keyboards import contact_button, question1, question2, question3
from config import *
import asyncio
import aiogram
from db_setting import database

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# voronka_id = 9317886


async def on_startup_notify(dispatcher: Dispatcher):
    try:
        await dispatcher.bot.send_message(827950639, "Бот Запущен")

    except Exception as err:
        await dispatcher.bot.send_message(827950639, text=f"{err}")


async def on_startup(dispatcher):
    database.create_table()
    await on_startup_notify(dispatcher)


@dp.message_handler(commands=['rs'])
async def broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id in [3325847, 6287458105, 827950639]:
        await state.set_state("broadcast")
        await message.reply("Текст, фото или видео для рассылки(1 штуку только).")
    else:
        await message.reply("Вы не админ.")


@dp.message_handler(content_types=types.ContentTypes.ANY, state="broadcast")
async def broadcast_handler(message: types.Message, state: FSMContext):
    tasks = []
    users = database.get_all_users()
    try:
        if message.photo:
            for i in users:
                await bot.send_message(i[0], "Hello")
                await bot.send_photo(
                    i[0],
                    message.photo[-1].file_id,
                    caption=message.caption
                )
        if message.video:
            for i in users:
                await bot.send_video(
                    i[0],
                    video=message.video.file_id,
                    caption=message.caption
                )
        if message.location:
            for i in users:
                await bot.send_location(
                    i[0],
                    latitude=message.location.latitude,
                    longitude=message.location.longitude
                )
        else:
            for i in users:
                await bot.send_message(
                    i[0],
                    message.text
                )
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        pass

    # await asyncio.gather(*tasks)
    await message.answer("Рассылка завершена!")
    await state.finish()


@dp.message_handler(CommandStart())
async def get_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args:
        await message.answer("📢 Рўйхатдан ўтганингиз учун рахмат! "
                             "Муҳим маълумотларни йўқотиб қўймаслик учун, илтимос, "
                             "бизнинг Telegram гуруҳимизга қўшилинг: "
                             "🔗 https://t.me/+tkXweoTohw1lODhi.")
        await message.answer(
            " Бизнинг вебинарга яхшироқ "
            "тайёргарлик кўриш учун, компаниянгизда нечта ходим ишлайди?",
            reply_markup=question1
        )
        msg = await message.answer("Илтимос, бироз кутинг ......")
        await Registration.num_emploeyes.set()
        d = args.split("--")
        l = {
            "name": d[0],
            "number": f"+{d[1]}"
        }
        database.insert_into(message.from_user.id, d[0], f"+{d[1]}")

        create_contact(d[0], d[1])
        lead_create_without_landing(d[1], d[1])
        await bot.delete_message(message.from_user.id, msg.message_id)
        await state.set_data(l)
    else:
        text = """📢 Ассалому алайкум! 26-март куни соат 14:00 да Барно Турсунова билан "Тўғри мотивация тизими ёрдамида компания фойдасини қандай ошириш мумкин" мавзусидаги вебинарга рўйхатдан ўтиш учун, илтимос, маълумотларингизни юборинг."""
        await message.answer(text=text)
        await message.answer(text="👤 Илтимос, исм ва фамилиянгизни киритинг.")
        await Registration.name.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Registration.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer(f"📞 Раҳмат, {data['name']}! Енди, илтимос, "
                             f"телефон рақамингизни пастдаги тугма орқали улашинг.", reply_markup=contact_button)
    await Registration.next()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Registration.phone)
async def get_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text or message.contact.phone_number
        create_contact(data['name'], data['number'])
        database.insert_into(message.from_user.id, data['name'], data['number'])
    await message.answer("📢 Рўйхатдан ўтганингиз учун рахмат, "
                         "Муҳим маълумотларни йўқотиб қўймаслик учун, илтимос, бизнинг Telegram гуруҳимизга қўшилинг: "
                         "🔗 https://t.me/+tkXweoTohw1lODhi. "
                         )
    await message.answer("Бизнинг вебинарга яхшироқ тайёргарлик кўриш учун, компаниянгизда нечта ходим ишлайди?",
                         reply_markup=question1)
    await Registration.next()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Registration.num_emploeyes)
async def get_num_emploeyes(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]
    async with state.proxy() as data:
        data['num_emploeyes'] = ans

    await call.message.answer("Раҳмат! Сизнинг компаниянгизнинг йиллик обороти қанча? "
                              "Бу маълумот вебинарга яхшироқ тайёргарлик кўриш учун керак.",
                              reply_markup=question2)
    await Registration.turnover.set()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Registration.turnover)
async def get_turnover(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]
    async with state.proxy() as data:
        data['turnover'] = ans
    await call.message.answer('Биз сизга ёрдам беришга деярли тайёрмиз. '
                              'Компанияда қандай ролни бажараётганингизни аниқлаб беринг 🌟',
                              reply_markup=question3)
    await Registration.role.set()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Registration.role)
async def get_turnover(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]

    async with state.proxy() as data:
        data['role'] = ans
        msg = await call.message.answer("Илтимос, бироз кутинг ......")
        contact_save(
            num_emploeyes=data['num_emploeyes'],
            turnover=data['turnover'],
            role=data['role'],
            number=data['number']
        )
        lead_create_without_landing(data['number'], data['number'])
        await call.message.answer("Жавобларингиз учун раҳмат! Биз ишонамизки, "
                                  "вебинаримиз айнан сиз учун мос. Вебинарда кўришгунча!")
        await bot.delete_message(call.message.from_user.id, msg.message_id)
    await state.finish()

    # await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
