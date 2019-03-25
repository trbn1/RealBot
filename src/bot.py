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

        try:
            self.status = config.get('Settings', 'status')
            if 'online' not in self.status and 'dnd' not in self.status:
                raise Exception('Status must be \'online\' or \'dnd\'.')
        except Exception as e:
            print('Error: Invalid status passed. %s' % e)
            sys.exit(1)

        self.emotes = config.get('ID', 'emotes').split(',')
        if '' in self.emotes:
            self.send_emotes = False

        else: 
            self.send_emotes = True

        self.quit_phrases = config.get('Settings', 'quit_phrases').split(',')
        if '' in self.quit_phrases:
            self.quit = False

        else: 
            self.quit = True

        self.concurrent_messages = {}
        self.invisible = False

        for channel_id in self.channels:
            self.bg_task = self.loop.create_task(self.background_task(channel_id))


    async def send_message(self, channel, message_type, mode='spam'):
        if self.invisible:
            return

        if mode is 'spam':
            self.concurrent_messages[int(channel.id)] += 1

        with channel.typing():
            await asyncio.sleep(self.typing_time)

            if message_type is 'text':
                msg = random.choice(self.messages)
                try:
                    await channel.send(msg)
                except:
                    print('Error while sending a message')

            if message_type is 'emote':
                try:
                    await channel.send(random.choice(self.emotes))
                except:
                    print('Error while sending a message')

        if self.quit and message_type is 'text':
            for sentence in self.quit_phrases:
                if sentence in msg:
                    await asyncio.sleep(1)
                    self.invisible = True
                    await self.change_presence(status='invisible')
                    await asyncio.sleep(random.randint(300, 3600))
                    self.invisible = False
                    await self.change_presence(status=self.status)
                    await asyncio.sleep(5)


    async def background_task(self, channel_id):
        await self.wait_until_ready()
        await self.change_presence(status=self.status)
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

            if random.randint(0, 100) < self.emote_chance and self.send_emotes:
                await self.send_message(channel, 'emote')

            if random.randint(0, 100) < self.combo_chance:
                await self.send_message(channel, 'text')
                await asyncio.sleep(random.randint(0, self.sleep_time))

            else:
                await asyncio.sleep(random.randint(0, self.sleep_time))


    async def on_message(self, message):
        if message.author.id is self.user.id or message.channel.id not in self.channels:
            return

        if '<@' + str(self.user.id) + '>' in message.content:
            channel = message.channel
            await self.send_message(channel, 'text', mode='reply')

            if random.randint(0, 100) < self.emote_chance and self.send_emotes:
                await self.send_message(channel, 'emote', mode='reply')


cfg.generate_config()
config = cfg.load_config()
client = MyClient()

try:
    client.run(config.get('Settings', 'token'))
except discord.errors.LoginFailure as e:
    print('Error: %s' % e)
    sys.exit(1)
