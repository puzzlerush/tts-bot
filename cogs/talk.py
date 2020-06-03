import discord
from discord.ext import commands
from discord.utils import get
from gtts import gTTS 
import os 

def create_audio(text, language, slowed):
    fname_prefix = 'audio_tmp'
    count = 1
    while fname_prefix + str(count) + '.mp3' in os.listdir('audio/'):
        count += 1
    fname = fname_prefix + str(count) + '.mp3'
    audio_file = gTTS(text=text, lang=language, slow=slowed)
    audio_file.save(f'audio/{fname}')
    return fname

def delete_audio(filename):
    os.remove(f'audio/{filename}')

class Talk(commands.Cog):
    DEFAULT_LANGUAGE = 'en'
    IS_SLOW = False
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        voice_client = get(self.client.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await ctx.send(f"Moved to {channel}")
        else:
            voice_client = await channel.connect()
            await ctx.send(f"Joined {channel}")

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.author.voice.channel
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.send(f"Left {channel}")
        else:
            await ctx.send(f"I'm not in a channel")
    
    @commands.command()
    async def say(self, ctx, *, msg):
        filename = create_audio(msg, self.DEFAULT_LANGUAGE, self.IS_SLOW)
        voice_client = get(self.client.voice_clients, guild=ctx.guild)
        print(filename)
        voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f'audio/{filename}'), after=lambda e: delete_audio(f'{filename}'))
        
    @commands.command()
    async def normal(self, ctx):
        self.IS_SLOW = False
        await ctx.send("I am going to speak normally")

    @commands.command()
    async def slow(self, ctx):
        self.IS_SLOW = True
        await ctx.send("I am going to speak slowly")

    @commands.command(aliases=['set langauge', 'set lang', 'sl', 'lang'])
    async def set_language(self, ctx, language):
        self.DEFAULT_LANGUAGE = language
        await ctx.send(f"Language set to '{language}'")
        
def setup(client):
    client.add_cog(Talk(client))
    
