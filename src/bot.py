# -*- coding: utf-8 -*-

import asyncio
import config as cfg
import discord
import random
import sys
from collections import namedtuple


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for arg in kwargs:
            self.name = kwargs[arg]

        try:
            with open(config.get(self.name, 'messages'), 'r', encoding='utf8') as f:
                self.messages = f.readlines()
        except:
            print('Error: Failed to open %s.' % config.get(self.name, 'messages'))
            sys.exit(1)

        try:
            self.channels = [int(val) for val in config.get(self.name, 'channel').split(',')]
        except:
            print('Error: Invalid channel ID passed.')
            sys.exit(1)

        try:
            self.sleep_time = int(config.get(self.name, 'sleep_time'))
            self.emote_chance = int(config.get(self.name, 'emote_chance'))
            self.combo_chance = int(config.get(self.name, 'combo_chance'))
            self.highlight_chance = int(config.get(self.name, 'highlight_chance'))
            self.typing_time = float(config.get(self.name, 'typing_time'))
            self.max_concurrent_messages = int(config.get(self.name, 'max_concurrent_messages'))
        except ValueError as e:
            print('Error: Invalid values in [Settings] section of configuration file. %s' % e)
            sys.exit(1)

        try:
            self.status = config.get(self.name, 'status')
            if 'online' not in self.status and 'dnd' not in self.status:
                raise Exception('Status must be \'online\' or \'dnd\'.')
        except Exception as e:
            print('Error: Invalid status passed. %s' % e)
            sys.exit(1)

        try:
            self.sleep_mode = config.get(self.name, 'sleep')
            if 'yes' not in self.sleep_mode and 'no' not in self.sleep_mode:
                raise Exception('Sleep mode must be \'yes\' or \'no\'.')

            if 'yes' in self.sleep_mode:
                self.sleep_mode = True

            else:
                self.sleep_mode = False
        except Exception as e:
            print('Error: Invalid sleep mode passed. %s' % e)
            sys.exit(1)

        self.emotes = config.get(self.name, 'emotes').split(',')
        if '' in self.emotes:
            self.send_emotes = False

        else: 
            self.send_emotes = True

        self.quit_phrases = config.get(self.name, 'quit_phrases').split(',')
        if '' in self.quit_phrases:
            self.quit = False

        else: 
            self.quit = True

        self.concurrent_messages = {}
        self.invisible = False
        self.highlight_ids = []

        try:
            self.names = []
            for section in config.sections():
                self.names.append(config.get(section, 'name'))
        except Exception as e:
            print('Error: invalid name passed. %s' % e)
            sys.exit(1)

        for channel_id in self.channels:
            self.bg_task = self.loop.create_task(self.background_task(channel_id))


    async def send_message(self, channel, message_type, mode='spam'):
        if self.invisible:
            return

        if mode is 'spam' and self.sleep_mode:
            self.concurrent_messages[int(channel.id)] += 1

        with channel.typing():
            await asyncio.sleep(self.typing_time)

            if message_type is 'text':
                msg = random.choice(self.messages)
                if random.randint(0, 100) < self.highlight_chance:
                    msg = random.choice(self.highlight_ids) + ' ' + msg
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
        first_loop = True

        for member in self.get_all_members():
            if member.name not in self.user.name and member.name in self.names:
                self.highlight_ids.append(member.mention)

        while not self.is_closed():
            if self.concurrent_messages[int(channel.id)] > self.max_concurrent_messages and self.max_concurrent_messages is not 0 and self.sleep_mode and not first_loop:
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

            elif first_loop:
                first_loop = False
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
            await asyncio.sleep(random.randint(2, 10))
            await self.send_message(channel, 'text', mode='reply')

            if random.randint(0, 100) < self.emote_chance and self.send_emotes:
                await self.send_message(channel, 'emote', mode='reply')


async def login():
    for i, e in enumerate(entries):
        try:
            await e.client.login(tokens[i])
        except discord.errors.LoginFailure as e:
            print('Error: %s' % e)
            sys.exit(1)

async def connect(entry):
    try:
        await entry.client.connect()
    except Exception as e:
        await entry.client.close()
        print('Error: ', e.__class__.__name__, e)
        entry.event.set()

# check if we should close the event loop
async def check_close():
    futures = [e.event.wait() for e in entries]
    await asyncio.wait(futures)

# load config
cfg.generate_bot_config()
config = cfg.load_config()

# attach clients to event
Entry = namedtuple('Entry', 'client event')
entries = []
tokens = []
for section_name in config.sections():
    entries.append(Entry(client=MyClient(name=section_name), event=asyncio.Event()))
    tokens.append(config.get(section_name, 'token'))

# create event loop
loop = asyncio.get_event_loop()

# login
loop.run_until_complete(login())

# connect every client
for e in entries:
    loop.create_task(connect(e))

# wait for all clients to close
loop.run_until_complete(check_close())

# close loop
loop.close()