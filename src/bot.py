# -*- coding: utf-8 -*-

import asyncio
import config as cfg
import discord
import random


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            with open(config.get('FilePaths', 'messages'), 'r', encoding='utf8') as f:
                self.messages = f.readlines()
        except:
            print('Error reading %s.' % config.get('FilePaths', 'messages'))
            exit(0)

        self.channels = [int(val) for val in config.get('ID', 'channel').split(',')]
        self.emotes = config.get('ID', 'emotes').split(',')

        self.sleep_time = int(config.get('Settings', 'sleep_time'))
        self.emote_chance = int(config.get('Settings', 'emote_chance'))
        self.combo_chance = int(config.get('Settings', 'combo_chance'))
        self.typing_time = float(config.get('Settings', 'typing_time'))

        self.bg_task = self.loop.create_task(self.background_task())


    async def background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(random.choice(self.channels))

        while not self.is_closed():
            with channel.typing():
                await asyncio.sleep(self.typing_time)
                await channel.send(random.choice(self.messages))

            if random.randint(0, 100) < self.emote_chance:
                with channel.typing():
                    await asyncio.sleep(self.typing_time)
                    await channel.send(random.choice(self.emotes))

            if random.randint(0, 100) < self.combo_chance:
                with channel.typing():
                    await asyncio.sleep(self.typing_time)
                    await channel.send(random.choice(self.messages))
                await asyncio.sleep(random.randint(0, self.sleep_time))

            else:
                channel = self.get_channel(random.choice(self.channels))
                await asyncio.sleep(random.randint(0, self.sleep_time))


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('<@' + str(self.user.id) + '>'):
            with message.channel.typing():
                await asyncio.sleep(self.typing_time)
                await message.channel.send(random.choice(self.messages).format(message))

            if random.randint(0, 100) < self.emote_chance:
                with message.channel.typing():
                    await asyncio.sleep(self.typing_time)
                    await message.channel.send(random.choice(self.emotes).format(message))


cfg.generate_config()
config = cfg.load_config()
client = MyClient()
client.run(config.get('Settings', 'token'))
