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

        self.concurrent_messages = {}

        for channel_id in self.channels:
            self.bg_task = self.loop.create_task(self.background_task(channel_id))


    async def send_message(self, channel, message_type, mode='spam'):
        if mode is 'spam':
            self.concurrent_messages[int(channel.id)] += 1

        with channel.typing():
            await asyncio.sleep(self.typing_time)

            if message_type is 'text':
                await channel.send(random.choice(self.messages))
            
            if message_type is 'emote':
                await channel.send(random.choice(self.emotes))


    async def background_task(self, channel_id):
        await self.wait_until_ready()
        channel = self.get_channel(channel_id)
        self.concurrent_messages[int(channel.id)] = self.max_concurrent_messages + 1

        while not self.is_closed():
            if self.concurrent_messages[int(channel.id)] > self.max_concurrent_messages and self.max_concurrent_messages is not 0:
                self.concurrent_messages[int(channel.id)] = 0
                start_spam_at_messages = random.randint(2, 10) # amount of message to wait for before starting spamming
                messages_counter = 0

                while True:
                    msg = await self.wait_for('message')

                    if int(msg.channel.id) is int(channel.id):
                        messages_counter += 1

                    if int(msg.channel.id) is int(channel.id) and messages_counter is start_spam_at_messages:
                        break
                        
                await asyncio.sleep(random.randint(0, self.sleep_time))

            await self.send_message(channel, 'text')

            if random.randint(0, 100) < self.emote_chance:
                await self.send_message(channel, 'emote')

            if random.randint(0, 100) < self.combo_chance:
                await self.send_message(channel, 'text')
                await asyncio.sleep(random.randint(0, self.sleep_time))

            else:
                await asyncio.sleep(random.randint(0, self.sleep_time))


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return            

        if '<@' + str(self.user.id) + '>' in message.content:
            channel = message.channel
            await self.send_message(channel, 'text', mode='reply')

            if random.randint(0, 100) < self.emote_chance:
                await self.send_message(channel, 'emote', mode='reply')


cfg.generate_config()
config = cfg.load_config()
client = MyClient()
client.run(config.get('Settings', 'token'))
