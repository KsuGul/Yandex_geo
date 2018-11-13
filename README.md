# Python-GeoBot  

Последовательность шагов по созданию телеграм-бота, который на вход получает файл geojson, а на выход отдает файл: 
описание какие объекты есть на карте и сколько их.

### BotFather
В Телеграме с помощью @BotFather создаем своего бота, получим от него токен.

## Python
### Установка + прототип
Установим библиотеку pyTelegramBotAPI для работы с Телеграм-ботом
   
    $ pip install pyTelegramBotAPI

Открываем bot.py, импортируем библиотеки и создаём главные переменные:
   
    import telebot
    import logging

    bot = telebot.TeleBot(TOKEN)
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)
Добавим логи, чтобы удобнее было отслеживать изменение статусов бота.

### Взаимодествие.Пример хендлера
Протестируем работу бота отправкой и получением текстовых сообщений с помощью следующего примера.
    
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        if message.text == "Hi":
            bot.send_message(message.from_user.id, "Hello! How can i help you?")

        elif message.text == "How are you?" or message.text == "How are u?":
            bot.send_message(message.from_user.id, "I'm fine, thanks. And you?")

        else:
            bot.send_message(message.from_user.id, "Sorry, i dont understand you.")
            
     bot.polling(none_stop=True, interval=0) 
     
### GeoJson 
Убедившись, что бот шлет сообщения в ответ, напишем хендлер для обработки документов

    @bot.message_handler(content_types=['document'])
    def command_handle_document(message):
        bot.send_message(message.from_user.id, "Документ получен")  
        
 Для того, чтобы убедиться, что geojson-файл корректно распознан ботом, выведем параметры и состав файла в ответ на файл 
 
    @bot.message_handler(content_types=['document'])
    def command_handle_document(message):
       raw = message.document.file_id
        path = str(raw+".geojson") 
        file_info = bot.get_file(raw)
        bot.send_message(message.from_user.id, str(file_info))    
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.from_user.id, str(downloaded_file))
        
  Подсчитаем количество геометрических объектов, которые хранятся в geojson, импортировав библиотеки и добавив следующий код в функцию:      
  
        import json
        from collections import Counter

        with open(path,'wb+') as new_file:
            new_file.write(downloaded_file)
        with open(str(new_file.name), encoding='utf8') as f:
            data = json.load(f)
        objects_type = [feature['geometry']['type'] for feature in data['features']]   
        result = dict(Counter(objects_type))
        bot.send_message(message.from_user.id, str(result))      
 В данной версии мы не поставили фильтр на обработку только geojson-файлов и не учли, что файл может быть некорректым.
 
### Добавление эксепшенов
Добавим фильтрацию на тип файла и сделаем эксепшн на случай, если geojson некорректен. Вынесем проверки в отдельную функцию, 
чтобы удобнее было покрывать тестами.

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

 ## Финальная версия
    
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

### GitHub/Heroku



