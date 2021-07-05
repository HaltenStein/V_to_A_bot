from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sql import SQL
from backend import creating_list_quality


TOKEN = ""  # your token 
MY_ID = 1  # your id in telegram

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


#greeting a new user
@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message) -> None:
    await message.answer(f"Hi {message.chat.first_name}!\n"+
                            "Shall we begin?\n"+
                            "Send a link from youtube to get the audio file")


#send message with helper commands list
@dp.message_handler(commands='help')
async def start_cmd_handler(message: types.Message) -> None:
    await message.answer("Send a link from youtube to get the audio file\n\n"+
                        "Do you want more high-quality audio or do you have any questions?\n"+
                        "Write to me @HaltenStein")


#processing button data (file quality or cancel)
@dp.callback_query_handler()
async def process_callback_qulity(callback_query: types.CallbackQuery):
    call = callback_query.data #inline button data
    if call == 'button1':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    else:
        await bot.send_message(callback_query.from_user.id, 'Please wait!')
        text = callback_query.message.text + ' ' + call + ' ' + str(callback_query.from_user.id)

        await bot.send_message(MY_ID, text)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        

@dp.message_handler(lambda message: message.text[:23] == "https://www.youtube.com"
                                        or message.text[:22] == "http://www.youtube.com"
                                        or message.text[:16] == "https://youtu.be"
                                        or message.from_user.id == MY_ID)
async def process_start_command(message: types.Message):
    if message.from_user.id != MY_ID:
        list_prime_id = SQL.select_prime_user()
        prime_id = any(message.from_user.id in id_tuple for id_tuple in list_prime_id)

        # inline buttom with affordable quality
        inline_kb = creating_list_quality(message.text, prime_id)
        await message.answer(message.text, reply_markup=inline_kb)
        await bot.delete_message(message.chat.id, message.message_id)
        
        #check user in 
        SQL.db_select_id(message.from_user.id)
    else:
        if message.text.isdigit():
            SQL.add_prime_user(int(message.text))
            await bot.send_message(MY_ID, f'id number {message.text} has received prime status')

        user_id, audio_id = message.text.split()
        await bot.send_audio(int(user_id), audio_id, caption='@V_to_A_bot')


@dp.message_handler(content_types=['audio'])
async def audio_response(message: types.Audio) -> None:
    """Function of receiving an audio track from the client and sending it to the user\n
    ID of the user who requested this track is in the track description before the first `@sfsf@`\n
    All other data after `@sfsf@` is divided by the same characters
    and loaded into the database to prevent the same file from being loaded a second time"""

    if message.from_user.id == MY_ID:
        file_id = message.audio.file_id

        message = message.caption.split('@sfsf@')
        id_addressee, title, duration, performer, quality = message
        SQL.db_insert_audio(file_id, title, int(duration), performer, quality)

        await bot.send_audio(id_addressee, file_id, caption='@V_to_A_bot')


if __name__ == '__main__':
    SQL.create_db()
    print("bot run")
    executor.start_polling(dp, skip_updates=True)
