import discord
from discord.ext import commands
import asyncio
import pyttsx3
import os

WORDS = {"соси" : [None, "Sam sosi XD"],
         "фистинг" : ["Fisting is 300.mp3", "mmmmm    eeeeeee"]

}

MAIN_PATH = "sounds/"

class MyClient(discord.Client):

    async def on_ready(self):

        self.voice_channel_list = []
        self.current_channel = None
        self.voice = None

        for guild in self.guilds:
            for channel in guild.voice_channels:
                if channel.id != 734866467128082475:
                    self.voice_channel_list.append(channel)
        # print(voice_channel_list)

        print('Logged on as {0}!'.format(self.user.display_name))
        await self.check()
    
    async def check(self):
        
        while self.current_channel == None:
            for ch in reversed(self.voice_channel_list):
                # if ch.id == 735524913590566921 and ch.members:
                #     await self.conn(ch)
                #     print(f"connected to -> {ch.name}")
                # elif ch.id == 734865236493991970 and ch.members:
                #     await self.conn(ch)
                #     print(f"connected to -> {ch.name}")
                if ch.members:
                    await self.conn(ch)
                    print(f"connected to -> {ch.name}")
            await asyncio.sleep(2)

    async def conn(self, ch):
            vc = await ch.connect()
            self.voice = vc
            self.current_channel = ch
            while self.current_channel != None:
                if len(ch.members) > 1:
                    await asyncio.sleep(2)
                else:
                    await self.voice.disconnect()
                    await asyncio.sleep(2)
                    self.voice = None
                    self.current_channel = None
                    await self.check()

    async def play_sound(self, content, typ):
        if self.voice != None:
            if typ == "sound":
                # print(f"{MAIN_PATH}{content}")
                self.voice.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=f"{MAIN_PATH}{content}"))
                while self.voice.is_playing():
                    await asyncio.sleep(.1)
            elif typ == "music":
                self.voice.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=f"{content}"))
                while self.voice.is_playing():
                    await asyncio.sleep(.1)
                

        else:
            await self.check()
            print("Bot not in voice room")

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
            if "play" in message.content.lower():
                content = message.content.lower()[5:]
                print(content)
                
               
client = MyClient()

# cl = commands.Bot(command_prefix="!")

# @cl.command(pass_context = True)
# async def play(ctx, url):
#     server = ctx.message.server
#     voice_client = cl.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url)
#     player.start()

token = os.environ.get("BOT_TOKEN")
client.run(str(token))
