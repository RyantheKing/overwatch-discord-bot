import discord
import sheets
from discord.utils import get
import json
from tabulate import tabulate
import http.client
from chatbot import demo
from chatbot import Chat, register_call
import re
import random
import requests
import json
from os import path

character_list = ['ana', 'ashe', 'baptiste', 'bastion', 'brigitte', 'dVa', 'doomfist', 'echo', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'sigma', 'soldier76', 'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston', 'wreckingball', 'zarya', 'zenyatta']
platform = 'pc'
region = 'us'
people_dict = {}
question = "Hi, how are you?"

def get_json_data(player, character):
    conn = http.client.HTTPSConnection("ow-api.com")
    if character == 'all':
        conn.request("GET", "/v1/stats/"+platform+'/'+region+'/'+player+'/profile')
    else:
        conn.request("GET", "/v1/stats/"+platform+'/'+region+'/'+player+'/heroes/'+character)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global question
        # don't respond to ourselves
        if message.author == self.user:
            return
        #if message.content.startswith('!make'):
        #    role = await message.channel.guild.create_role(name="This doesn't give me admin")
        #    await message.author.add_roles(role)
        if not message.content.startswith(',compare'): message.content = message.content.lower()
        if message.content == 'ping' and message.channel.id == 833896814645739580:
            await message.channel.send('pong')
        elif message.content == 'unping' and message.channel.id == 833896814645739580:
            await message.channel.send("pongn't")
        elif message.content.startswith('!psy'):
            question = "Hi, how are you?"
            await message.channel.send(question)
        elif message.content.startswith("!"):
            question = Chat("d:/Documents/Code/Overwatch bot/Chatbot/examples/Example.template").converse(message.content[1:], question) 
            await message.channel.send(question)
        elif message.content.startswith(',compare'):
            compare_list = message.content.split()[1:]
            if compare_list[-1] in character_list: character = compare_list[-1]
            else: character = 'all'
            player_data_list = [get_json_data(player, character) for player in compare_list[0:-1]]
            new_data = tabulate([
                ['Rating']+[str(data['rating'])+' sr' for data in player_data_list],
                ['Win Rate']+[str(int(int(data['competitiveStats']['games']['won'])/int(data['competitiveStats']['games']['played'])*100))+'%' for data in player_data_list]],
                headers=['Stats ('+character+')']+[data['name'] for data in player_data_list],
                tablefmt="grid")
            await message.channel.send('```\n'+new_data+' ```')
        elif message.content.startswith(',heroes') and message.channel.id == 833896814645739580:
            remainder = ' '.join(message.content.split()[1:])
            if remainder.startswith('l'):
                await message.channel.send(sheets.return_hero_comp('lij'))
            elif remainder.startswith('han'):
                await message.channel.send(sheets.return_hero_comp('han'))
            elif remainder.startswith('nu'):
                await message.channel.send(sheets.return_hero_comp('num'))
            elif remainder.startswith('j'):
                await message.channel.send(sheets.return_hero_comp('jun'))
            elif remainder.startswith('i'):
                await message.channel.send(sheets.return_hero_comp('ill'))
            elif remainder.startswith('t'):
                await message.channel.send(sheets.return_hero_comp('tem'))
            elif remainder.startswith('e'):
                await message.channel.send(sheets.return_hero_comp('eic'))
            elif remainder.startswith('w'):
                await message.channel.send(sheets.return_hero_comp('wat'))
            elif remainder.startswith('bu'):
                await message.channel.send(sheets.return_hero_comp('bus'))
            elif remainder.startswith('v'):
                await message.channel.send(sheets.return_hero_comp('vol'))
            elif remainder.startswith('k'):
                await message.channel.send(sheets.return_hero_comp('kin'))
            elif remainder.startswith('ro'):
                await message.channel.send(sheets.return_hero_comp('rou'))
            elif remainder.startswith('ne'):
                await message.channel.send(sheets.return_hero_comp('nep'))
            elif remainder.startswith('ho'):
                await message.channel.send(sheets.return_hero_comp('hol'))
            elif remainder.startswith('d'):
                await message.channel.send(sheets.return_hero_comp('dor'))
            elif remainder.startswith('o'):
                await message.channel.send(sheets.return_hero_comp('oas'))
            elif remainder.startswith('bl'):
                await message.channel.send(sheets.return_hero_comp('bli'))
            elif remainder.startswith('hav'):
                await message.channel.send(sheets.return_hero_comp('hav'))
            elif remainder.startswith('ri'):
                await message.channel.send(sheets.return_hero_comp('ria'))
            else:
                await message.channel.send('Invalid Map Identifier')
        elif (message.content.startswith(',')) and message.channel.id == 833896814645739580:
            contents = message.content.lower().split()
            if contents[-2] == 'win':
                column = 1
            elif contents[-2] == 'loss':
                column = 2
            elif contents[-2] == 'tie' and contents[-2] == 'draw':
                column = 3
            else:
                await message.channel.send('Invalid match outcome status')
            map = ' '.join(contents[:-2])
            if map.startswith('lij'):
                await message.add_reaction('👍')
                sheets.updateStat('lij', column)
            elif map.startswith('han'):
                await message.add_reaction('👍')
                sheets.updateStat('han', column)
            elif map.startswith('num'):
                await message.add_reaction('👍')
                sheets.updateStat('num', column)
            elif map.startswith('jun'):
                await message.add_reaction('👍')
                sheets.updateStat('jun', column)
            elif map.startswith('ill'):
                await message.add_reaction('👍')
                sheets.updateStat('ill', column)
            elif map.startswith('tem'):
                await message.add_reaction('👍')
                sheets.updateStat('tem', column)
            elif map.startswith('eic'):
                await message.add_reaction('👍')
                sheets.updateStat('eic', column)
            elif map.startswith('wat'):
                await message.add_reaction('👍')
                sheets.updateStat('wat', column)
            elif map.startswith('bus'):
                await message.add_reaction('👍')
                sheets.updateStat('bus', column)
            elif map.startswith('vol'):
                await message.add_reaction('👍')
                sheets.updateStat('vol', column)
            elif map.startswith('kin'):
                await message.add_reaction('👍')
                sheets.updateStat('kin', column)
            elif map.startswith('rou'):
                await message.add_reaction('👍')
                sheets.updateStat('rou', column)
            elif map.startswith('nep'):
                await message.add_reaction('👍')
                sheets.updateStat('nep', column)
            elif map.startswith('hol'):
                await message.add_reaction('👍')
                sheets.updateStat('hol', column)
            elif map.startswith('dor'):
                await message.add_reaction('👍')
                sheets.updateStat('dor', column)
            elif map.startswith('oas'):
                await message.add_reaction('👍')
                sheets.updateStat('oas', column)
            elif map.startswith('bli'):
                await message.add_reaction('👍')
                sheets.updateStat('bli', column)
            elif map.startswith('hav'):
                await message.add_reaction('👍')
                sheets.updateStat('hav', column)
            elif map.startswith('ria'):
                await message.add_reaction('👍')
                sheets.updateStat('ria', column)
            else:
                await message.add_reaction('🚫')
                sheets.updateStat('unk', column)

client = MyClient()
client.run('<client sercret here>')