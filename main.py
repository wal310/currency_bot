import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='b!', intents=intents)
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.lower() == 'hello' or message.content.lower() == 'hi':
    await message.channel.send(f'hello there {message.author.name}')
  else:
    await bot.process_commands(message)

@bot.command(help='displays player balance', brief='displays player balance')
async def balance(ctx):
  await open_account(ctx.author)
  users = await get_data()
  balance = str(users[str(ctx.author.id)])
  em = discord.Embed(title=f"{ctx.author.name}", color=discord.Color.blue())
  em.add_field(name="balance", value=balance)
  await ctx.channel.send(embed=em)


@bot.command(help='transfers amount to account', brief='transfers amount to account')
async def change(ctx, amount):
  await open_account(ctx.author)
  users = await get_data()
  new_balance = users[str(ctx.author.id)] + int(amount)
  if new_balance < 0:
    await ctx.channel.send("you cannot take out more money than you have")
    return False
  users[str(ctx.author.id)] = new_balance
  await write_data(users)

@bot.command(help='shuts down bot', brief='shuts down bot')
async def shutdown(ctx):
  to_leave = bot.get_guild(976645645907681290)
  await to_leave.leave()

async def open_account(user):
  users = await get_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = 0
  await write_data(users)
  return True

async def get_data():
  with open('user_data.json', 'r') as file:
    users = json.load(file)
  return users


async def write_data(users):
  with open('user_data.json', 'w') as file:
    json.dump(users, file)
bot.run(TOKEN)