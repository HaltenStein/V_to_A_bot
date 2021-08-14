from os import remove
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
from telethon import events
from backend import download_from_yt


API_ID_CONF = 1  # your id clients in telegram
API_HASH_CONF = ""  # your hash clients in telegram
client = TelegramClient('anon', API_ID_CONF, API_HASH_CONF)
client.start()


@client.on(events.NewMessage(chats='V_to_A_bot'))
async def in_client(event):
    url, quality, user_id = event.message.to_dict()['message'].split()

    file, yt, flag = download_from_yt(url, quality)
    if flag:
        duration = yt.length
        title = yt.title
        performer = yt.author
        caption = str(user_id)+'@sfsf@'+title+'@sfsf@'+str(duration)+'@sfsf@'+performer+'@sfsf@'+quality
        await client.send_file(
                    entity='V_to_A_bot',
                    file=file,
                    caption=caption,
                    attributes=[DocumentAttributeAudio(
                                                duration=duration,
                                                title=title,
                                                performer=performer)])
        remove(file)
    else: 
        await client.send_message('V_to_A_bot', user_id+' '+file[0][0])


print("client run")  
client.run_until_disconnected()
