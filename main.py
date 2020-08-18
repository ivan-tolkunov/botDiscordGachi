#! /usr/bin/env python
# -*- coding: utf-8 -*- // 


# Надо для работы в линуксе русских символов


import discord
import asyncio
import pyttsx3
import os


WORDS = {"соси" : [None, "Sam sosi XD"],
         "фистинг" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
         "пенетрайшн" : ["8 differet Penetrationsounds.wav", "mmmmm    eeeeeee"],
         "анал" : ["Anal.wav", "mmmmm    eeeeeee"],
         "сее" : ["Do you like what you see.mp3", "mmmmm    eeeeeee"],
         "данжн" : ["Dungeon master.mp3", "mmmmm    eeeeeee"],
         "300" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
         "фак" : ["FUCK YOU.wav", "mmmmm    eeeeeee"],
         "слейвс" : ["Fuckin Slaves.wav", "mmmmm    eeeeeee"],
         "дееп" : ["It's so fucking deep.mp3", "mmmmm    eeeeeee"],
         "камм" : ["Make me cum.wav", "mmmmm    eeeeeee"],
         "сори" : ["Oh Shit Im Sorry.wav", "mmmmm    eeeeeee"],
         "фор" : ["Sorry for what.wav", "mmmmm    eeeeeee"],
         "каминг" : ["Ooouuuuh Im fucking cumming.wav", "mmmmm    eeeeeee"],
         "фингер" : ["Stick your finger.mp3", "mmmmm    eeeeeee"],
         "сволов" : ["Swallow my cum.mp3", "mmmmm    eeeeeee"],
         "бой" : ["Take it boy.mp3", "mmmmm    eeeeeee"],

        #  "suck" : [None, "Sam sosi XD"],
        #  "fisting" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "penetrationsounds" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "анал" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "сее" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "данжн" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "300" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "фак" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "слейвс" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "каминг" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "дееп" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "камм" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "сори" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "камингг" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "фингер" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "сволов" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],
        #  "бой" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"],


} # Добавляю словарь команд

MAIN_PATH = "sounds/" # Указываю путь к папке с звуками

class MyClient(discord.Client): # Создаю класс бота

    async def on_ready(self): # Функция выполняется при запуске бота

        self.voice_channel_list = [] # Создаю переменные обьекта
        self.current_channel = None
        self.voice = None

        for guild in self.guilds:
            for channel in guild.voice_channels:
                if channel.id != 734866467128082475:
                    self.voice_channel_list.append(channel) # Беру список всех голосовых каналов кроме афк и записываю в переменную
        # print(voice_channel_list)

        print('Logged on as {0}!'.format(self.user.display_name))
        await self.check() # Запускаю выполнение функции проверки
    
    async def check(self): # Функция проверки
        
        while self.current_channel == None: # Пока бот не зашел не в один канал
            for ch in reversed(self.voice_channel_list): # идем по списку каналов в обратном порядке, чтобы главной был первым
                if ch.members: # Если в канале есть люди
                    await self.conn(ch) # Вызываем функцию подключения
                    print(f"connected to -> {ch.name}")
            await asyncio.sleep(2) # Ждем 2 секунды

    async def conn(self, ch): # Функция подключения
            vc = await ch.connect() 
            self.voice = vc
            self.current_channel = ch # Подключаемся к каналу
            while self.current_channel != None: # Пока подключены
                if len(ch.members) > 1: # 
                    await asyncio.sleep(2)
                else:
                    await self.voice.disconnect()
                    await asyncio.sleep(2)
                    self.voice = None
                    self.current_channel = None
                    await self.check()

    async def on_message(self, message):
        if message.author != self.user:
            for key in WORDS:
                if key in message.content.lower():
                    i = 0
                    for item in WORDS[key]:
                        if i == 0:
                            if item != None:
                                if self.current_channel != None:
                                    await self.play_sound(item, "sound")
                        else:
                            await message.channel.send(item)
                        i+=1

    async def play_sound(self, content, typ):
        if self.voice != None:
            if typ == "sound":
                # print(f"{MAIN_PATH}{content}")
                self.voice.play(discord.FFmpegPCMAudio(source=f"{MAIN_PATH}{content}"))
                while self.voice.is_playing():
                    await asyncio.sleep(.1)   
        else:
            await self.check()
            print("Bot not in voice room")
                
               
client = MyClient()
token = os.environ.get("BOT_TOKEN")
client.run(str(token))
