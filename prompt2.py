#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 17:41:47 2018

@author: ksu
"""
import telebot
import json
from collections import Counter
import logging
import os

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(content_types=['document'])
def command_handle_document(message):
    raw = message.document.file_id  
    filename, file_extension = os.path.splitext(str(message.document.file_name))
    path = str(raw+file_extension) 
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb+') as new_file:
        new_file.write(downloaded_file)
    result = geojson_processing(new_file)
    bot.send_message(message.from_user.id, str(result))    

def geojson_processing(file):
    try:
        filename, file_extension = os.path.splitext(str(file.name))
        if file_extension == '.geojson':
            with open(str(file.name), encoding='utf8') as f:
                data = json.load(f)
            objects_type = [feature['geometry']['type'] for feature in data['features']]   
            return dict(Counter(objects_type))           
        else:
            return "Ошибка: исходный файл - не geojson"
    except ValueError:
        return "Ошибка: geojson файл некорректый"
          
bot.polling(none_stop=True, interval=0) 



