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
        self.max_concurrent_messages = int(config.get('Settings', 'max_concurrent_messages'))

        self.concurrent_messages = 0

        self.bg_task = self.loop.create_task(self.background_task())


    async def send_message(self, channel, message_type):
        self.concurrent_messages += 1
        with channel.typing():
            await asyncio.sleep(self.typing_time)

            if message_type is 'text':
                await channel.send(random.choice(self.messages))
            
            if message_type is 'emote':
                await channel.send(random.choice(self.emotes))


    async def background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(random.choice(self.channels))

        while not self.is_closed():
            if self.concurrent_messages > self.max_concurrent_messages and self.max_concurrent_messages is not 0:
                self.concurrent_messages = 0
                await self.wait_for('message')
                await asyncio.sleep(random.randint(0, self.sleep_time))

            await self.send_message(channel, 'text')

            if random.randint(0, 100) < self.emote_chance:
                await self.send_message(channel, 'emote')

            if random.randint(0, 100) < self.combo_chance:
                await self.send_message(channel, 'text')
                await asyncio.sleep(random.randint(0, self.sleep_time))

            else:
                channel = self.get_channel(random.choice(self.channels))
                await asyncio.sleep(random.randint(0, self.sleep_time))


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return            

        if message.content.startswith('<@' + str(self.user.id) + '>'):
            channel = message.channel
            await self.send_message(channel, 'text')

            if random.randint(0, 100) < self.emote_chance:
                await self.send_message(channel, 'emote')


cfg.generate_config()
config = cfg.load_config()
client = MyClient()
client.run(config.get('Settings', 'token'))
