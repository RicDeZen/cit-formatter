import subprocess
import pathlib
import json
import discord_downloader

from pathlib import Path
from discord_downloader import DiscordDownloader

CONFIG_FILE = Path("config.json")

config = json.load(CONFIG_FILE.open("r"))

dce_path = Path(config["dce_path"]).resolve()
token = config["discord_token"]
channel = config["discord_channel_id"]
dwn_path = Path(config["download_path"])
# Making sure download dir exists
if not dwn_path.exists():
    dwn_path.mkdir()
dwn_path = dwn_path.resolve()

DiscordDownloader(dce_path, token).download_channel(channel, dwn_path)

print("Ay lmao my dude, done 100%.")