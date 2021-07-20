from pytube import YouTube
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from sql import SQL


def download_from_yt(url, quality):
    yt = YouTube(url)

    # checking the file for presence in the database
    id_audio = SQL.db_check_audio(yt.title, yt.length,
                                yt.author, quality)

    if len(id_audio) == 0: # there was no such file before
        file = yt.streams.filter(only_audio=True, abr=quality).first().download()

        # rename file in .mp3
        if 'mp4' in file:
            old_f = '4pm'
        else:
            old_f = 'mbew'
        new_file = file[::-1].replace(old_f, '3pm', 1)[::-1]
        os.rename(file, new_file)
        flag = True
    else:
        new_file = id_audio
        flag = False
    return new_file, yt, flag


def creating_list_quality(url: str, prime: bool) -> InlineKeyboardButton:
    yt = YouTube(url)
    list_yt = yt.streams.filter(only_audio=True)

    inline_btn = InlineKeyboardButton('Cancel', callback_data='button1')
    inline_kb_full = InlineKeyboardMarkup(row_width=1).add(inline_btn)

    low_quality = any(('50kbps' or '70kbps') in data_file.abr for data_file in list_yt)

    for data_file in list_yt:
        if not prime and low_quality and ('50kbps' == data_file.abr or '70kbps' == data_file.abr):
            inline_kb_full.add(InlineKeyboardButton(data_file.abr, callback_data=data_file.abr))
        elif prime or not low_quality:
            inline_kb_full.add(InlineKeyboardButton(data_file.abr, callback_data=data_file.abr))  
    return inline_kb_full
