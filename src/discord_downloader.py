import subprocess
from pathlib import Path

CONFIG_FILE = Path("config.json")

class ChatDownloader():
    '''
    Class to download a Discord server channel's data, requires
    DiscordChatExporter to be installed.
    '''
    def __init__(self, dce_path : Path, token : str):
        '''
        Parameters:
            dce_path : Path
                The Path to the DiscordCharExported executable file
            token : str
                The Discord account token
        '''
        super().__init__()
        if not dce_path.exists() : raise ValueError("Path for DCE does not exist.")
        self.dce = dce_path.resolve()
        self.token = token

    def download_channel(self, channel : str, output : Path, output_type="plaintext") -> None:
        '''
        Download a channel's history

        Parameters:
            channel : str
                The target channel's ID.
            output : Path
                output directory or file.
            output_type : str (default = "plaintext")
                Type of output file. See DCE for details.
        '''
        if not output.exists() : raise ValueError("Path for output does not exist.")
        output = output.resolve()
        command = "{} export -o {} -t {} -c {} -f {}".format(self.dce, output, self.token, channel, output_type)
        subprocess.run(command)