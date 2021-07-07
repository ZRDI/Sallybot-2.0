import discord
import random
from flask import Flask
from discord.ext import commands
from SimpleEconomy import Seco 

#keepalive
from threading import Thread
app = Flask('Sallybot')
@app.route('/')
def home():
	return 'ENGAGING TACTICAL THERMONUCLEAR CLUSTER STRIKE MISSILE'
def run():
	app.run(host='0.0.0.0',port=8080)
def keep_alive():
	t = Thread(target=run)
	t.start()

TOKEN = 'ODQwNTkzOTM1ODk3ODUzOTc0.YJaeGw.3EzJmYglk3upe9fl-S08eHTStQ0'
bot = commands.Bot(command_prefix = 's?')
seco = Seco(bot,'96AisadaxTt6TcYnCNi1b48VOVojAGpD6Utazngs01Vj7c2iT0plAgnHjFiLc4eo','sallycoin',logs=True) 
bot.remove_command('help')

@bot.event
async def on_ready():
	print('Online')
	await bot.change_presence(activity = discord.Game(name = 's?help'))

#balance
@bot.command(name = 'bal')
async def bal(ctx):
	balance = await seco.get_balance(ctx.author.id)
	balembed = discord.Embed(title ='Pocket Balance', color = 0xffff00, description = f'You have {balance} sallycoins in your pocket!')
	balembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
	balembed.set_footer(text = 'Sallycoins in your pocket!')
	balembed.set_thumbnail(url = 'https://pngimg.com/uploads/coin/coin_PNG36887.png')
	await ctx.send(embed = balembed)

#bankbal
@bot.command(name = 'bankbal')
async def bankbal(ctx):
	balance = await seco.get_bank(ctx.author.id)
	bankembed = discord.Embed(title ='Sallybank Balance', color = 0xffff00, description = f'You have {balance} sallycoins in your sallybank!')
	bankembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
	bankembed.set_footer(text = 'Sallycoins in your sallybank!')
	bankembed.set_thumbnail(url = 'https://pngimg.com/uploads/coin/coin_PNG36887.png')
	await ctx.send(embed = bankembed)

#deposit
@bot.command(name = 'deposit')
async def deposit(ctx, argdep):
  pocketamt = await seco.get_balance(ctx.author.id) 
  if int(argdep) > int(pocketamt):
    depfail1embed = discord.Embed(title = 'Deposit', color = 0xffff00, description = 'You cannot deposit that much sallycoins into your sallybank!')
    depfail1embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    depfail1embed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = depfail1embed)
  elif int(argdep) < 0:
    depfail2embed = discord.Embed(title = 'Deposit', color = 0xffff00, description = 'You cannot deposit negative sallycoins into your sallybank!')
    depfail2embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    depfail2embed.set_footer(text = 'Could not deposit sallycoins!')
    depfail2embed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = depfail2embed)
  else:
    depembed = discord.Embed(title = 'Deposit', color = 0xffff00, description = f'You have deposited {argdep} sallycoins in your sallybank!')
    depembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    depembed.set_footer(text = 'Sallycoins deposited!')
    depfail1embed.set_footer(text = 'Could not deposit sallycoins!')
    depembed.set_thumbnail(url = 'https://pngimg.com/uploads/coin/coin_PNG36887.png')
    await seco.remove_balance(ctx.author.id, int(argdep))
    await seco.add_bank(ctx.author.id, int(argdep))
    await ctx.send(embed = depembed)

#beg
@bot.command(name = 'beg')
@commands.cooldown(1, 5, commands.BucketType.user)
async def beg(ctx):
	sentencelist = ['Sally pitied you and gave you ', 'Sally donated ', 'Sally dropped some sallycoins and you picked up ']
	sentence = random.choice(sentencelist)
	begnum = random.randint(1, 10)
	begsentence = sentence + str(begnum) + ' sallycoins!'
	await seco.add_balance(ctx.author.id, int(begnum))
	begembed = discord.Embed(title = 'Beg', color = 0xffff00, description = begsentence)
	begembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
	begembed.set_footer(text = 'Sallycoins!')
	begembed.set_thumbnail(url = 'https://pngimg.com/uploads/coin/coin_PNG36887.png')
	await ctx.send(embed = begembed)

@beg.error
async def beg(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        begwarn = discord.Embed(title = 'You cannot use this command too fast! Slow down!', color = 0xffff00, description = f'Try again in {error.retry_after:.2f} seconds!')
        await ctx.send(embed = begwarn)

#withdraw
@bot.command(name = 'withdraw')
async def withdraw(ctx, argwith):
  bankamt = await seco.get_bank(ctx.author.id)
  if int(argwith) > int(bankamt):
    withfail1embed = discord.Embed(title = 'Deposit', color = 0xffff00, description = 'You cannot withdraw that much sallycoins from your sallybank!')
    withfail1embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    withfail1embed.set_footer(text = 'Could not withdraw sallycoins!')
    await ctx.send(embed = withfail1embed)
  elif int(argwith) < 0:
    withfail2embed = discord.Embed(title = 'Deposit', color = 0xffff00, description = 'You cannot withdraw negative sallycoins from your sallybank!')
    withfail2embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    withfail2embed.set_footer(text = 'Could not withdraw sallycoins!')
    withfail1embed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    withfail2embed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = withfail2embed)
  else:
    withembed = discord.Embed(title = 'Withdraw', color = 0xffff00, description = f'You have withdrawed {argwith} sallycoins from your sallybank!')
    withembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    withembed.set_footer(text = 'Sallycoins withdrawn!')
    withembed.set_thumbnail(url = 'https://pngimg.com/uploads/coin/coin_PNG36887.png')
    await seco.remove_bank(ctx.author.id, int(argwith))
    await seco.add_balance(ctx.author.id, int(argwith))
    await ctx.send(embed = withembed)


#shop
@bot.command(name = 'shop')
async def shop(ctx, shoppg):
  if shoppg == '1':
    pocketamt = await seco.get_balance(ctx.author.id)
    shopembed1 = discord.Embed(title = 'Sally Shop (Page 1/1)', color = 0xffff00, description = f'Buy something from the shop! You have {pocketamt} sallycoins to spend!')
    shopembed1.add_field(name = 'Sally Plush (10 sallycoins)', value = 'A fluffy Sally plush to squish!')
    shopembed1.set_footer(text = 'Buy something from Sally Shop!')
    shopembed1.set_thumbnail(url = 'https://www.pngkey.com/png/full/410-4109417_carrinho-de-compras-creative-online-shopping-logo.png')
    await ctx.send(embed = shopembed1)
  else:
    pgfailembed = discord.Embed(title = 'Invalid page number!', color = 0xffff00, description = 'Whoops!')
    pgfailembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    pgfailembed.set_footer(text = 'Uh oh...')
    pgfailembed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = pgfailembed)

#bet
@bot.command(name = 'bet')
async def bet(ctx, betnum):
  betreal = random.randint(1, 10)
  if int(betnum) == int(betreal):
    betembed = discord.Embed()
    



#share 
@bot.command(name = 'share')
async def share(ctx, amt, target):
  pocketamt = await seco.get_balance(ctx.author.id)
  targetid = int(target[3:len(target)-1])
  if int(amt) < 0:
    sharefailembed1 = discord.Embed(title = 'Share', color = 0xffff00, description = 'Hey! Sharing negative sallycoins is stealing! Try entering a positive number instead!')
    sharefailembed1.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    sharefailembed1.set_footer(text = 'Try s?rob instead!')
    sharefailembed1.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = sharefailembed1)
  elif pocketamt < int(amt):
    sharefailembed2 = discord.Embed(title = 'Share', color = 0xffff00, description = 'You do not have enough sallycoins in your pocket to share that much sallycoins!')
    sharefailembed2.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    sharefailembed2.set_footer(text = 'Not enough sallycoins in pocket!')
    sharefailembed2.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = sharefailembed2)
  elif targetid == ctx.author.id:
    sharefailembed3 = discord.Embed(title = 'Share', color = 0xffff00, description = 'You cannot share money with yourself!')
    sharefailembed3.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    sharefailembed3.set_footer(text = 'What are you doing?!?!?!')
    sharefailembed3.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = sharefailembed3)
  elif int(amt) == 0:
    sharefailembed3 = discord.Embed(title = 'Share', color = 0xffff00, description = 'Why are you sharing nothing?')
    sharefailembed3.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    sharefailembed3.set_footer(text = 'Huh?')
    sharefailembed3.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
  else:
    shareembed = discord.Embed(title = 'Share', color = 0xffff00, description = f'You shared {amt} sallycoins with {target}!')
    shareembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    shareembed.set_footer(text = 'Sharing is caring!')
    shareembed.set_thumbnail(url = 'https://www.pngkey.com/png/full/35-350233_image-information-handshake-logo-transparent.png')
    await ctx.send(embed = shareembed)
    await seco.remove_balance(ctx.author.id, int(amt))
    await seco.add_balance(targetid, int(amt))



#help
@bot.command(name = 'help')
async def help(ctx):
  helpembed = discord.Embed(title = 'Help', color = 0xffff00, description = 'This is the help page!')
  helpembed.add_field(name = 's?admin [page number]', value = 'Shows all admin commnds!', inline = False)
  helpembed.add_field(name = 's?fun [page number]', value = 'Shows all fun commands!', inline = False)
  helpembed.add_field(name = 's?reaction [page number]', value = 'Shows all reaction commands!', inline = False)
  helpembed.add_field(name = 's?game [page number]', value = 'Shows all game commands!', inline = False)
  helpembed.set_footer(text = 'Getting some help!')
  helpembed.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
  await ctx.send(embed = helpembed)

#admin help
@bot.command(name = 'admin')
async def admin(ctx, adminpg):
  if adminpg == '1':
    adminembed1 = discord.Embed(title = 'Admin Commands Help (Page 1/1)', color = 0xffff00, description = 'This is the admin commands help page!')
    adminembed1.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    adminembed1.set_footer(text = 'Admin stuff!')
    adminembed1.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
    await ctx.send(embed = adminembed1)
  else:
    pgfailembed = discord.Embed(title = 'Invalid page number!', color = 0xffff00, description = 'Whoops!')
    pgfailembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    pgfailembed.set_footer(text = 'Uh oh...')
    pgfailembed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = pgfailembed)

#fun help
@bot.command(name = 'fun')
async def fun(ctx, funpg):
  if funpg == '1':
    funembed1 = discord.Embed(title = 'Fun Commands Help (Page 1/1)', color = 0xffff00, description = 'This is the fun commands help page!')
    funembed1.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    funembed1.set_footer(text = 'Getting some help!')
    funembed1.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
    await ctx.send(embed = funembed1)
  else:
    pgfailembed = discord.Embed(title = 'Invalid page number!', color = 0xffff00, description = 'Whoops!')
    pgfailembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    pgfailembed.set_footer(text = 'Uh oh...')
    pgfailembed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = pgfailembed)


#reaction help
@bot.command(name = 'reaction')
async def reaction(ctx, reactionpg):
  if reactionpg == '1':
    reactionembed1 = discord.Embed(title = 'Reaction Commands Help (Page 1/1)', color = 0xffff00, description = 'This is the reaction commands help page!')
    reactionembed1.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    reactionembed1.set_footer(text = 'Getting some help!')
    reactionembed1.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
    await ctx.send(embed = reactionembed1)
  else:
    pgfailembed = discord.Embed(title = 'Invalid page number!', color = 0xffff00, description = 'Whoops!')
    pgfailembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    pgfailembed.set_footer(text = 'Uh oh...')
    pgfailembed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = pgfailembed)

#game help
@bot.command(name = 'game')
async def game(ctx, gamepg):
  if gamepg == '1':
    gameembed1 = discord.Embed(title = 'Game Commands Help (Page 1/2)', color = 0xffff00, description = 'This is the game commands help page!')
    gameembed1.add_field(name = 's?bal', value = 'Checks how much sallycoins you have in your pocket!', inline = False)
    gameembed1.add_field(name = 's?bankbal', value = 'Checks how much sallycoins you have in your sallybank!', inline = False)
    gameembed1.add_field(name = 's?deposit [amount]', value = 'Deposits [amount] of sallycoins into your sallybank!', inline = False)
    gameembed1.add_field(name = 's?withdraw [amount]', value = 'Withdraws [amount] of sallycoins from your sallybank!', inline = False)
    gameembed1.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    gameembed1.set_footer(text = 'Getting some help!')
    gameembed1.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
    await ctx.send(embed = gameembed1)
  elif gamepg == '2':
    gameembed2 = discord.Embed(title = 'Game Commands Help (Page 2/2)', color = 0xffff00, description = 'This is the game commands help page!')
    gameembed2.add_field(name = 's?beg', value = 'Beg to get 1 to 10 sallycoins!', inline = False)
    gameembed2.add_field(name = 's?shop [page number]', value = 'Shows the Sally Shop where you can buy items!', inline = False)
    gameembed2.add_field(name = 's?share [amount] [personping]', value = 'Shares [amount] of sallycoins with [personping]! (e.g: s?share 10 @sally)', inline = False)
    gameembed2.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    gameembed2.set_footer(text = 'Getting some help!')
    gameembed2.set_thumbnail(url = 'https://www.pngkey.com/png/full/285-2858358_you-may-have-some-questions-about-debate-yellow.png')
    await ctx.send(embed = gameembed2) 
  else:
    pgfailembed = discord.Embed(title = 'Invalid page number!', color = 0xffff00, description = 'Whoops!')
    pgfailembed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    pgfailembed.set_footer(text = 'Uh oh...')
    pgfailembed.set_thumbnail(url = 'http://www.pngall.com/wp-content/uploads/4/Exclamation-Mark-Symbol-PNG.png')
    await ctx.send(embed = pgfailembed)

keep_alive()
bot.run(TOKEN)



