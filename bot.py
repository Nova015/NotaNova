import discord
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ID_ASISTENCIA = os.getenv("ID_CANAL_ASISTENCIA ")
ID_UPDATE = os.getenv("ID_CANAL_UPDATE")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

scheduler = AsyncIOScheduler()

#@client.event
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

    if not scheduler.running:
        scheduler.add_job(enviar_recordatorios, 'cron', day_of_week='tue', hour=15, minute=20)
        scheduler.start()


def cargar_mensaje(nombre_archivo):
    ruta_completa = os.path.join("recordatorios", nombre_archivo)
    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        return archivo.read()

async def enviar_recordatorios():
    print("¡Recordatorio programado ejecutado!") 
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    canal_update = bot.get_channel(ID_UPDATE)

    mensaje_avance = cargar_mensaje("mensaje_avance.txt")
    mensaje_junta = cargar_mensaje("mensaje_junta.txt")

    if canal_asistencia:
        await canal_asistencia.send(mensaje_avance)
    if canal_update:
        await canal_update.send(mensaje_junta)

@bot.command()
async def testbot(ctx):
    await ctx.send("Eviando mensajes de prueba")
    await enviar_recordatorios()
bot.run(TOKEN)
#client.run(TOKEN)

