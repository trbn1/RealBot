# -*- coding: utf-8 -*-

import asyncio
import config as cfg
import discord
import random
import sys


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            with open(config.get('FilePaths', 'messages'), 'r', encoding='utf8') as f:
                self.messages = f.readlines()
        except:
            print('Error: Failed to open %s.' % config.get('FilePaths', 'messages'))
            sys.exit(1)

        try:
            self.channels = [int(val) for val in config.get('ID', 'channel').split(',')]
        except:
            print('Error: Invalid channel ID passed.')
            sys.exit(1)
        
        try:
            self.sleep_time = int(config.get('Settings', 'sleep_time'))
            self.emote_chance = int(config.get('Settings', 'emote_chance'))
            self.combo_chance = int(config.get('Settings', 'combo_chance'))
            self.typing_time = float(config.get('Settings', 'typing_time'))
            self.max_concurrent_messages = int(config.get('Settings', 'max_concurrent_messages'))
        except ValueError as e:
            print('Error: Invalid values in [Settings] section of configuration file. %s' % e)
            sys.exit(1)

        self.emotes = config.get('ID', 'emotes').split(',')
        self.quit_phrases = config.get('Settings', 'quit_phrases').split(',')

        self.concurrent_messages = {}
        self.status = 0

        for channel_id in self.channels:
            self.bg_task = self.loop.create_task(self.background_task(channel_id))


    async def send_message(self, channel, message_type, mode='spam'):
        if self.status is 1:
            return

        if mode is 'spam':
            self.concurrent_messages[int(channel.id)] += 1

        with channel.typing():
            await asyncio.sleep(self.typing_time)

            if message_type is 'text':
                msg = random.choice(self.messages)
                await channel.send(msg)
            
            if message_type is 'emote' and self.emotes is not '':
                await channel.send(random.choice(self.emotes))

        for sentence in self.quit_phrases:
            if sentence in msg and self.quit_phrases is not '' and message_type is 'text':
                await asyncio.sleep(1)
                self.status = 1
                await self.change_presence(status='invisible')
                await asyncio.sleep(random.randint(300, 3600))
                self.status = 0
                await self.change_presence(status='dnd')
                await asyncio.sleep(5)


    async def background_task(self, channel_id):
        await self.wait_until_ready()
        await self.change_presence(status='dnd')
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
        if message.author.id is self.user.id:
            return

        if '<@' + str(self.user.id) + '>' in message.content:
            channel = message.channel
            await self.send_message(channel, 'text', mode='reply')

            if random.randint(0, 100) < self.emote_chance:
                await self.send_message(channel, 'emote', mode='reply')


cfg.generate_config()
config = cfg.load_config()
client = MyClient()

try:
    client.run(config.get('Settings', 'token'))
except discord.errors.LoginFailure as e:
    print('Error: %s' % e)
    sys.exit(1)
