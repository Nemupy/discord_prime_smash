import disnake
from disnake.ext import commands
import random


bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())


def judge(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def factor(n):
    a = 1
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            if n // i > a:
                a = n // i
            else:
                break
    b = n // a
    return a, b


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        n = int(reaction.message.content)
        if str(reaction.emoji) == "⭕":
            if judge(n) == True:
                await reaction.message.delete()
            if judge(n) == False:
                await reaction.message.remove_reaction(reaction, user)
        if str(reaction.emoji) == "❌":
            if judge(n) == True:
                await reaction.message.remove_reaction(reaction, user)
            if judge(n) == False:
                await reaction.message.delete()
                a, b = factor(n)
                messageA = await reaction.message.channel.send(a)
                messageB = await reaction.message.channel.send(b)
                await messageA.add_reaction("⭕")
                await messageA.add_reaction("❌")
                await messageB.add_reaction("⭕")
                await messageB.add_reaction("❌")


@bot.command()
async def start(ctx, min=100, max=200):
    n = random.randint(min, max)
    message = await ctx.send(n)
    await message.add_reaction("⭕")
    await message.add_reaction("❌")


bot.run("UR_TOKEN")
