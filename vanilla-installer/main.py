PATH_FILE = 'data/mc-path.txt'

import os
import logging
import requests
import minecraft_launcher_lib as mll

def set_dir(path: str):
    """Sets the Minecraft game directory.

    Args:
        path (str): THe path to the Minecraft game directory.
    """
    return open(PATH_FILE, 'w').write(path)

def get_dir() -> str:
    """Returns the Minecraft game directory.

    Returns:
        str: Path
    """
    return open(PATH_FILE).read()
            
def newest_version() -> str:
    return mll.utils.get_latest_version()['release']
            
def get_java() -> str:
    return mll.utils.get_java_executable()

def init() -> None:
    if not os.path.exists(PATH_FILE): # sets the default Minecraft path automatically
        try:
            path = mll.utils.get_minecraft_directory()
        except Exception as e: # any error could happen, really.
            logging.error(f'Could not get Minecraft path: {e}')
            set_dir()
        else:
            set_dir(path)

def text_update(text: str, widget=None, color: str='fg') -> None:
    if widget:
        widget['text'] = text
        widget['fg'] = color
    else:
        logging.info(text)

def download_fabric(widget=None): # https://github.com/max-niederman/fabric-quick-setup/blob/40c959c6cd2295c679576680fab3cda2b15222f5/fabric_quick_setup/cli.py#L69 (nice)
    installers = requests.get('https://meta.fabricmc.net/v2/versions/installer').json()
    download = requests.get(installers[0]['url'])
    file_path = 'temp/' + download.url.split('/')[-1]
    
    text_update(f'Downloading Fabric ({int(download.headers["Content-Length"])//1000} KB)...', widget)
    open(file_path, 'wb').write(download.content)
    
    return file_path

def install_fabric(installer_jar: str, mc_version: str, mc_dir: str, widget=None): # installs the Fabric launcher jar
    text_update('Installing Fabric...', widget)
    ran = os.system(f'{get_java()} -jar {installer_jar} client -mcversion {mc_version} -dir {mc_dir}')
    
    if ran == 0:
        text_update(f'Installed Fabric: {ran}', widget)
    else:
        text_update(f'Could not install Fabric: {ran}', widget, 'error')

def download_pack(widget=None):
    text_update(f'Fetching Pack...', widget)

    pack_json = requests.get('https://api.github.com/repos/Fabulously-Optimized/fabulously-optimized/releases/latest').json()
    pack_file = ''
     
    for asset in pack_json['assets']:
        url = asset['browser_download_url']
        if 'MultiMC' in url:
            pack_file = url
            break
    
    download = requests.get(pack_file)
    text_update(f'Downloading Pack ({int(download.headers["Content-Length"])//1000} KB)...', widget)
    open(file_path, 'wb').write(download.content)

    os.makedirs(f'{get_dir}/', exist_ok=True)
    

def run(widget=None) -> None:
    """Starts the installation process.
    """
    text_update('Starting Fabric Download...', widget)
    installer_jar = download_fabric(widget=widget)
    text_update('Starting Fabric Installation...', widget)
    install_fabric(installer_jar=installer_jar, mc_version=newest_version(), mc_dir=get_dir(), widget=widget)

init() # start initialization