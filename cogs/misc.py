import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def ping(self, ctx):
        milliseconds = int(self.client.latency * 1000)
        await ctx.send(f"{milliseconds}ms")
        if milliseconds > 500:
            await ctx.send("Looks like I just suffered a MASSIVE DDOS attack right there...\n" +
                           "Not a whole lot you can do about that guys...")
        elif milliseconds > 200:
            await ctx.send("Looks like I just suffered a DDOS attack right there...\n" +
                           "Not a whole lot you can do about that guys...")
            
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}")

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#") 
        for entry in banned_users:
            user = entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return

def setup(client):
    client.add_cog(Misc(client))
