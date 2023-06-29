import sys
sys.path.append('../')

import discord
import disc.bot as bot
import libs.db as db
import libs.env as env

@bot.bot.command(guildids=[env.GUILD_ID], description="通話開始通知を行うデフォルトのチャンネルを変更します。")
async def change_default_notice_channel(ctx, text_ch:discord.TextChannel):
    msg = f"デフォルトの通知先を{text_ch.name}に変更しました。"
    await ctx.respond(msg)
    db.change_or_add_notice_channel("default", str(text_ch.id))
    bot.notice_channels = db.get_all_notice_channel_ids()
    bot.log(f"Slash_change_default_notice_ch: {text_ch.name}")

@bot.bot.command(guildids=[env.GUILD_ID], description="ボイスチャンネルの通知先を個別に設定します。")
async def change_notice_channel(ctx, voice_ch:discord.VoiceChannel, text_ch:discord.TextChannel):
    msg = f"{voice_ch.name}の通知先を{text_ch.name}に変更しました。"
    await ctx.respond(msg)
    db.change_or_add_notice_channel(str(voice_ch.id), str(text_ch.id))
    bot.notice_channels = db.get_all_notice_channel_ids()
    bot.log(f"Slash_change_notice_ch: {text_ch.name} <- {voice_ch.name}")
    

@bot.bot.command(guildids=[env.GUILD_ID], description="ボイスチャンネルの通知先をデフォルトに戻します。")
async def change_notice_ch_to_default(ctx, voice_ch:discord.VoiceChannel):
    msg = f"{voice_ch.name}の通知先をデフォルトのチャンネルに変更しました。"
    await ctx.respond(msg)
    db.delete_db_row(str(voice_ch.id))
    bot.notice_channels = db.get_all_notice_channel_ids()
    bot.log(f"Slash_change_notice_ch_to_default: {voice_ch.name}")