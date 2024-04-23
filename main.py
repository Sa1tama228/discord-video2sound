import os
import discord
from discord.ext import commands
import moviepy.editor
from pathlib import Path

if not os.path.exists('uploads'):
    os.makedirs('uploads')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='_', intents=intents)  # bot prefix is: _


@bot.command()
async def upload(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            save_path = Path('uploads') / attachment.filename
            try:
                await attachment.save(save_path)

                vid = moviepy.editor.VideoFileClip(str(save_path))
                audio = vid.audio
                audio_file_path = save_path.with_suffix('.mp3')
                audio.write_audiofile(str(audio_file_path))

                await ctx.send(f"File {attachment.filename} saved and loading now...")
                file = discord.File(audio_file_path)
                await ctx.send(file=file)
            except Exception as e:
                await ctx.send(f"Error processing attachment {attachment.filename}: {str(e)}")
    else:
        await ctx.send("No file detected!")

bot.run('YOU_BOT_TOKEN_IS_HERE')
