from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from states import Registration, Questioning
from utils import contact_save, create_contact, lead_create_without_landing
from keyboards import contact_button, question1, question2, question3, ha
from config import *

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
voronka_id = 9317886


@dp.message_handler(CommandStart())
async def get_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    if args == "1":
        await message.answer("Deeplink")
        await message.answer("Рахмат, энди, телефон опросдан отинг.")
        await message.answer("📢 Рўйхатдан ўтганингиз учун рахмат, {{name}}! "
                             "Муҳим маълумотларни йўқотиб қўймаслик учун, илтимос, бизнинг Telegram гуруҳимизга қўшилинг: "
                             "🔗 https://t.me/+tkXweoTohw1lODhi. Keyingi savollarga javob berishga tayormisiz",
                             reply_markup=question1)
        await Questioning.num_emploeyes.set()
        l = {
            "from_landing": 1,
        }
        await state.set_data(l)
    else:
        text = """📢 Assalomu alaykum! 
        26-mart kuni soat 14:00 da Barno Tursunova bilan "To‘g‘ri motivatsiya tizimi yordamida kompaniya foydasini qanday 
        oshirish mumkin" mavzusidagi vebinarga ro‘yxatdan o‘tish uchun, iltimos, ma'lumotlaringizni yuboring."""
        await message.answer(text=text)
        await message.answer(text="👤 Iltimos, ism va familiyangizni kiriting.")
        await Registration.name.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Registration.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer(f"📞 Rahmat, {data["name"]}! Endi, iltimos, telefon "
                             f"raqamingizni pastdagi tugma orqali ulashing.", reply_markup=contact_button)
    await Registration.next()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Registration.phone)
async def get_number(message: types.Message, state: FSMContext):
    number = None
    async with state.proxy() as data:
        data['number'] = message.text or message.contact.phone_number
        number = data['number']
        create_contact(data['name'], data['number'])
    await message.answer("📢 Рўйхатдан ўтганингиз учун рахмат, {{name}}! "
                         "Муҳим маълумотларни йўқотиб қўймаслик учун, илтимос, бизнинг Telegram гуруҳимизга қўшилинг: "
                         "🔗 https://t.me/+tkXweoTohw1lODhi. Keyingi savollarga javob berishga tayormisiz",
                         reply_markup=question1)
    await state.finish()
    await Questioning.num_emploeyes.set()
    d = {
        "number": number,
        "from_landing": 0,
    }
    await state.set_data(d)




@dp.message_handler(CommandStart(deep_link="1"))
async def start_with(message: types.Message, state: FSMContext):
    await message.answer("Deeplink")
    await message.answer("Рахмат, энди, телефон опросдан отинг.")
    await Questioning.num_emploeyes.set()
    l = {
        "from_landing": 1,
    }
    await state.set_data(l)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Questioning.num_emploeyes)
async def get_num_emploeyes(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]
    async with state.proxy() as data:
        print(data)
        if data['from_landing'] == 1:
            data['num_emploeyes'] = ans
        else:
            data['from_landing'] = 0
            data['num_emploeyes'] = ans

    await call.message.answer("Раҳмат! Сизнинг компаниянгизнинг йиллик обороти қанча? "
                              "Бу маълумот вебинарга яхшироқ тайёргарлик кўриш учун керак.",
                              reply_markup=question2)
    await Questioning.next()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Questioning.turnover)
async def get_turnover(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]
    async with state.proxy() as data:
        data['turnover'] = ans
    await call.message.answer('Биз сизга ёрдам беришга деярли тайёрмиз. '
                              'Компанияда қандай ролни бажараётганингизни аниқлаб беринг 🌟',
                              reply_markup=question3)
    await Questioning.next()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("q_"), state=Questioning.role)
async def get_turnover(call: types.CallbackQuery, state: FSMContext):
    ans = call.data.split("_")[1]
    async with state.proxy() as data:
        data['role'] = ans
        if data["from_landing"] == 1:
            await call.message.answer("Для убеждения введите номер телефона", reply_markup=contact_button)
            await Questioning.asking_number.set()
        else:
            contact_save(
                num_emploeyes=data['num_emploeyes'],
                turnover=data['turnover'],
                role=data['role'],
                number=data['number']
            )
            lead_create_without_landing(data['number'], data['number'])
            await call.message.answer("Жавобларингиз учун раҳмат! Биз ишонамизки, "
                                      "вебинаримиз айнан сиз учун мос. Вебинарда кўришгунча!")
            await state.finish()

    # await state.finish()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Questioning.asking_number)
async def additional(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Спасибо, увидимся на семинаре")
        phone = message.contact.phone_number or message.text
        contact_save(
            num_emploeyes=data['num_emploeyes'],
            turnover=data['turnover'],
            role=data['role'],
            number=phone
        )
        lead_create_without_landing(phone, phone)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
