import subprocess
import pathlib
import json
from src import *

from pathlib import Path
from src.discord_downloader import ChatDownloader
from src.discord_parser import QuoteParser
from src.latex_converter import *

CONFIG_FILE = Path("config.json")

config = json.load(CONFIG_FILE.open("r"))

dce_path = Path(config["dce_path"]).resolve()
if not dce_path.exists():
    raise ValueError("Can't find DCE")
token = config["discord_token"]
channel = config["discord_channel_id"]
dwn_path = Path(config["download_path"])
# Making sure download dir exists
if dwn_path.is_dir() and not dwn_path.exists():
    dwn_path.mkdir()
dwn_path = dwn_path.resolve()
if not Path("output/").exists():
    Path("output/").mkdir()

ChatDownloader(dce_path, token).download_channel(channel, dwn_path, "json")

data = json.load(dwn_path.open("r"))
quotes = QuoteParser().parse(data, config["aliases"])

grouped = group_msg_by_author(quotes)
print(grouped)
DocMaker().makedoc(
    grouped, "Le Cit-Cogne", "By Le Cicogne"
).generate_pdf("output/output", clean_tex=False)


print("Ay lmao my dude, done 100%.")
